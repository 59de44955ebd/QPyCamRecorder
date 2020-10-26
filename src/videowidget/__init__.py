from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

import os
import struct

from ctypes import oledll, windll, byref, cast, c_int, c_void_p, POINTER
from ctypes.wintypes import DWORD, LONG, ULONG, HWND, UINT, LPCOLESTR, LCID, LPVOID, MSG

from comtypes import client, IUnknown, Structure, GUID, COMMETHOD, HRESULT, BSTR, COMError, COMObject
from comtypes.server import IClassFactory
from comtypes.hresult import *

from comtypes.gen.DirectShowLib import (
		IAMVideoCompression,
		IBaseFilter,
		ICreateDevEnum,
		IFileSinkFilter,
		IFilterGraph,
		IGraphBuilder,
		IPropertyBag,
		IVMRAspectRatioControl,	VMR_ARMODE_LETTER_BOX, VMR_ARMODE_NONE
		)

from uuid import UUID

from videowidget.constants import *
from videowidget.interfaces import *
from videowidget.vmr9 import *

FILTER_DIR = os.path.dirname(os.path.realpath(__file__))+'\\filters'

INDEX_SPOUTCAM = 900
INDEX_SCREENCAM = 901

########################################
#
########################################
class MyPropertyPageSite (COMObject):
	_com_interfaces_ = [IPropertyPageSite]

########################################
#
########################################
class VideoWidget (QWidget):

	mousePressed = pyqtSignal(int,int)
	mouseDoubleClicked = pyqtSignal(int,int)

	########################################
	# @constructor
	########################################
	def __init__(self, parent=None):
		super().__init__(parent)
		self._reset()
		self._hwnd = self.winId().__int__()
		self._system_device_enum = client.CreateObject(CLSID_SystemDeviceEnum, interface=ICreateDevEnum)
		self._size_factor = self.devicePixelRatio()
		self._fullscreen = False
		self._prop_obj_filter = None
		self._prop_obj_pin = None

	########################################
	#
	########################################
	def _reset(self):
		self._cam = None
		self._cam_pin_out = None
		self._windowless_control = None
		self._filter_config = None
		self._vmr9 = None
		self._media_control = None
		self._graph_builder = None
		self._filter_graph = None
		self._page = None

	########################################
	#
	########################################
	def _create_interfaces (self):
		self._filter_graph = client.CreateObject(CLSID_FilterGraph, interface=IFilterGraph)
		self._graph_builder = self._filter_graph.QueryInterface(IGraphBuilder)
		self._media_control = self._filter_graph.QueryInterface(IMediaControl)

	########################################
	#
	########################################
	def _get_pin_by_name (self, filt, pinName):
		enum = filt.EnumPins()
		while True:
			pin, fetched = enum.Next(1)
			if not fetched: break
			pinInfo = pin.QueryPinInfo()
			if pinName in ''.join(map(chr, pinInfo.achName)):
				return pin

	########################################
	#
	########################################
	def _get_unconnected_pin (self, filt, direction):
		enum = filt.EnumPins()
		while True:
			pin, fetched = enum.Next(1)
			if not fetched: break
			d = pin.QueryDirection()
			if d==direction:
				try:
					tmp = pin.ConnectedTo() # Already connected - not the pin we want
				except:
					return pin

	########################################
	# Returns touple (out, in) or None
	########################################
	def _get_connected_pins (self, filt):
		enum = filt.EnumPins()
		while True:
			pin, fetched = enum.Next(1)
			if not fetched: break
			d = pin.QueryDirection()
			if d==PIN_DIR_OUT:
				try:
					return pin, pin.ConnectedTo()
				except: pass

	########################################
	# Given a string GUID, return the GUID laid out in memory suitable
	# for passing to ctypes
	########################################
	def _raw_guid (self, guid):
		return UUID(str(guid)).bytes_le

	########################################
	#
	########################################
	def _create_object_from_path (self, clsid, dll_filename, interface=IBaseFilter):
		iclassfactory = self._raw_guid(IClassFactory._iid_)
		my_dll = oledll.LoadLibrary(dll_filename)
		factory_ptr = c_void_p(0)
		hr = my_dll.DllGetClassObject(self._raw_guid(clsid), iclassfactory, byref(factory_ptr))
		if hr!=S_OK:
			raise COMError(hr, '', '')
		ptr_icf = POINTER(IClassFactory)(factory_ptr.value)
		unk = ptr_icf.CreateInstance()

		# if ScreenCam or SpoutCam is loaded from local file, we also grab its property page
		if clsid==CLSID_ScreenCam or clsid==CLSID_SpoutCam:
			factory_ptr = c_void_p(0)
			hr = my_dll.DllGetClassObject(
					self._raw_guid(CLSID_SpoutCamPropertyPage if clsid==CLSID_SpoutCam else CLSID_ScreenCamPropertyPage),
					iclassfactory,
					byref(factory_ptr))
			if hr!=S_OK:
				raise COMError(hr, '', '')
			ptr_icf = POINTER(IClassFactory)(factory_ptr.value)
			unk2 = ptr_icf.CreateInstance()
			self._page = unk2.QueryInterface(IPropertyPage)
		return unk.QueryInterface(interface)

	########################################
	# Saves DIB as BMP file
	########################################
	def _save_dib (self, filename, dib):
		with open(filename, 'wb') as f:
			# parse DIB header
			biSize, w, h, planes, bpp = struct.unpack('I 2i 2H', dib[:16])
			header_size = 14
			file_size = header_size + len(dib)
			offset = header_size + biSize
			header = struct.pack('<2s I 2H I', b'BM', file_size, 0, 0, offset)
			f.write(header)
			f.write(dib)
			return True
		return False

	########################################
	#
	########################################
	def _resize (self, w, h):
		if self._windowless_control is None:
			return False
		try:
			r = RECT(0, 0, int(w*self._size_factor), int(h*self._size_factor))
			self._windowless_control.SetVideoPosition(None, byref(r))
			return True
		except:
			return False

	########################################
	# Returns list of filter names
	########################################
	def _get_available_filters (self, category_clsid):
		filter_enumerator = self._system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
		moniker, fetched = filter_enumerator.RemoteNext(1)
		result = []
		while fetched > 0:
			result.append(self._get_moniker_name(moniker))
			moniker, fetched = filter_enumerator.RemoteNext(1)
		return result

	########################################
	# Returns (<filter guid>, <filter name>) or None
	########################################
	def _get_filter_by_index (self, category_clsid, filter_index):
		filter_enumerator = self._system_device_enum.CreateClassEnumerator(GUID(category_clsid), dwFlags=0)
		moniker, fetched = filter_enumerator.RemoteNext(1)
		i = 0
		while fetched > 0:
			if i==filter_index:
				return moniker.RemoteBindToObject(0, 0, IBaseFilter._iid_).QueryInterface(IBaseFilter), self._get_moniker_name(moniker)
			moniker, fetched = filter_enumerator.RemoteNext(1)
			i = i + 1

	########################################
	#
	########################################
	def _get_moniker_name (self, moniker):
		property_bag = moniker.RemoteBindToStorage(0, 0, IPropertyBag._iid_).QueryInterface(IPropertyBag)
		return property_bag.Read('FriendlyName', pErrorLog=None)

	########################################
	#
	########################################
	def set_filter_settings_container (self, container):
		self._filter_settings_container = container
		self._hwnd_filter_settings = container.winId().__int__()

	########################################
	#
	########################################
	def set_pin_settings_container (self, container):
		self._pin_settings_container = container
		self._hwnd_pin_settings = container.winId().__int__()

	########################################
	#
	########################################
	def load_video_device (self, idx):
		self._create_interfaces()
		if idx==INDEX_SPOUTCAM:
			self._cam, name = self._create_object_from_path(CLSID_SpoutCam, FILTER_DIR+'\\SpoutCam.ax'), 'SpoutCam'
		elif idx==INDEX_SCREENCAM:
			self._cam, name = self._create_object_from_path(CLSID_ScreenCam, FILTER_DIR+'\\ScreenCam.dll'), 'ScreenCam'
		else:
			self._cam, name = self._get_filter_by_index(CLSID_VideoInputDeviceCategory, idx)
		self._filter_graph.AddFilter(self._cam, name)

		# Find an output pin on the device filter
		self._cam_pin_out = self._get_unconnected_pin(self._cam, PIN_DIR_OUT)
		if self._cam_pin_out is None:
			self._reset()
			return False

		try:
			# Add Video Mixing Renderer
			self._vmr9 = client.CreateObject(CLSID_VideoMixingRenderer9, interface = IBaseFilter)
			self._filter_graph.AddFilter(self._vmr9, 'Video Mixing Renderer 9')
			self._filter_config = self._vmr9.QueryInterface(IVMRFilterConfig9)
			hr = self._filter_config.SetRenderingMode(VMR9Mode_Windowless)
			self._windowless_control = self._vmr9.QueryInterface(IVMRWindowlessControl9)
			r = RECT(0, 0, int(self.width()*self._size_factor), int(self.height()*self._size_factor))
			self._windowless_control.SetVideoPosition(None, byref(r))
			self._windowless_control.SetVideoClippingWindow(self._hwnd)

			# Render the output pin
			self._graph_builder.Render(self._cam_pin_out)

			self.set_keepaspectratio()
			self._media_control.Run()
			return True
		except COMError as e:
			print('COMError', str(e))
			self._reset()
			return False

	########################################
	#
	########################################
	def record_video_device_avi (self, avi_file, idx_video, idx_audio=-1):

		self._create_interfaces()
		if idx_video==INDEX_SPOUTCAM:
			self._cam, name = self._create_object_from_path(CLSID_SpoutCam, FILTER_DIR+'\\SpoutCam.ax'), 'SpoutCam'
		elif idx_video==INDEX_SCREENCAM:
			self._cam, name = self._create_object_from_path(CLSID_ScreenCam, FILTER_DIR+'\\ScreenCam.dll'), 'ScreenCam'
		else:
			self._cam, name = self._get_filter_by_index(CLSID_VideoInputDeviceCategory, idx_video)
		self._filter_graph.AddFilter(self._cam, name)

		# Find an output pin on the filter
		self._cam_pin_out = self._get_unconnected_pin(self._cam, PIN_DIR_OUT)
		if self._cam_pin_out is None:
			self._reset()
			return False

		try:
			# MJPEG Compressor
			mjpegCompressor = client.CreateObject(CLSID_MJPEGCompressor, interface = IBaseFilter)
			self._filter_graph.AddFilter(mjpegCompressor, 'MJPEG Compressor')

			# AVI Muxer
			aviMuxer = client.CreateObject(CLSID_AVIMuxer, interface = IBaseFilter)
			self._filter_graph.AddFilter(aviMuxer, 'AVI Muxer')

			# File Writer
			fileWriter = client.CreateObject(CLSID_FileWriter, interface = IBaseFilter)
			self._filter_graph.AddFilter(fileWriter, 'File Writer')

			# Set dest filename
			sink = fileWriter.QueryInterface(IFileSinkFilter)
			sink.SetFileName(avi_file, None)

			# Connect
			pin_mjpeg_in = self._get_pin_by_name(mjpegCompressor, 'Input')
			pin_mjpeg_out = self._get_pin_by_name(mjpegCompressor, 'Output')

			try:
				self._filter_graph.ConnectDirect(self._cam_pin_out, pin_mjpeg_in, None)
			except:
				# Direct connection failed, so try intelligent connect
				self._graph_builder.Connect(self._cam_pin_out, pin_mjpeg_in)

			self._filter_graph.ConnectDirect(pin_mjpeg_out, self._get_pin_by_name(aviMuxer, 'Input'), None)
			self._filter_graph.ConnectDirect(self._get_pin_by_name(aviMuxer, 'AVI Out'), self._get_pin_by_name(fileWriter, 'in'), None)

			# Use best MJPEG quality
			try:
				# Specifies the quality as a value between 0.0 and 1.0, where 1.0 indicates the best quality
				videoCompression = pin_mjpeg_out.QueryInterface(IAMVideoCompression)
				videoCompression.put_Quality(1.0)
			except: pass

			if idx_audio>=0:
				audio_source, name = self._get_filter_by_index(CLSID_AudioInputDeviceCategory, idx_audio)
				self._filter_graph.AddFilter(audio_source, name)
				pin_audio_out =  self._get_unconnected_pin(audio_source, PIN_DIR_OUT)
				pin_muxer_in =  self._get_unconnected_pin(aviMuxer, PIN_DIR_IN)
				try:
					self._filter_graph.ConnectDirect(pin_audio_out, pin_muxer_in, None)
				except:
					self._graph_builder.Connect(pin_audio_out, pin_muxer_in)

			self.set_keepaspectratio()
			self._media_control.Run()
			return True
		except COMError as e:
			print('COMError', str(e))
			self._reset()
			return False

	########################################
	#
	########################################
	def record_video_device_mp4 (self, mp4_file, idx_video, idx_audio=-1):

		self._create_interfaces()
		if idx_video==INDEX_SPOUTCAM:
			self._cam, name = self._create_object_from_path(CLSID_SpoutCam, FILTER_DIR+'\\SpoutCam.ax'), 'SpoutCam'
		elif idx_video==INDEX_SCREENCAM:
			self._cam, name = self._create_object_from_path(CLSID_ScreenCam, FILTER_DIR+'\\ScreenCam.dll'), 'ScreenCam'
		else:
			self._cam, name = self._get_filter_by_index(CLSID_VideoInputDeviceCategory, idx_video)
		self._filter_graph.AddFilter(self._cam, name)

		# Find an output pin on the filter
		self._cam_pin_out = self._get_unconnected_pin(self._cam, PIN_DIR_OUT)
		if self._cam_pin_out is None:
			self._reset()
			return False

		try:
			os.chdir(FILTER_DIR)

			# CSIR VPP H264 Encoder
			h264Encoder = self._create_object_from_path(CLSID_CSIRVPPH264Encoder, FILTER_DIR+'\\H264EncoderFilter.dll')
			self._filter_graph.AddFilter(h264Encoder, 'CSIR VPP H264 Encoder')

			# MPC Matroska Muxer
			mp4Muxer = self._create_object_from_path(CLSID_MPCMatroskaMuxer, FILTER_DIR+'\\MatroskaMuxer.ax')
			self._filter_graph.AddFilter(mp4Muxer, 'MPC Matroska Muxer')

			# File Writer
			fileWriter = client.CreateObject(CLSID_FileWriter, interface = IBaseFilter)
			self._filter_graph.AddFilter(fileWriter, 'File Writer')

			# Set dest filename
			sink = fileWriter.QueryInterface(IFileSinkFilter)
			sink.SetFileName(mp4_file, None)

			# Connect
			pin_h264Encoder_in = self._get_unconnected_pin(h264Encoder, PIN_DIR_IN)
			pin_h264Encoder_out = self._get_unconnected_pin(h264Encoder, PIN_DIR_OUT)

			try:
				self._filter_graph.ConnectDirect(self._cam_pin_out, pin_h264Encoder_in, None)
			except:
				# Direct connection failed, so try intelligent connect
				self._graph_builder.Connect(self._cam_pin_out, pin_h264Encoder_in)

			self._filter_graph.ConnectDirect(pin_h264Encoder_out, self._get_unconnected_pin(mp4Muxer, PIN_DIR_IN), None)
			self._filter_graph.ConnectDirect(self._get_unconnected_pin(mp4Muxer, PIN_DIR_OUT), self._get_pin_by_name(fileWriter, 'in'), None)

			if idx_audio>=0:
				audio_source, name = self._get_filter_by_index(CLSID_AudioInputDeviceCategory, idx_audio)
				self._filter_graph.AddFilter(audio_source, name)
				pin_audio_out = self._get_unconnected_pin(audio_source, PIN_DIR_OUT)
				pin_muxer_in = self._get_unconnected_pin(mp4Muxer, PIN_DIR_IN)
				try:
					self._filter_graph.ConnectDirect(pin_audio_out, pin_muxer_in, None)
				except:
					self._graph_builder.Connect(pin_audio_out, pin_muxer_in)

			self.set_keepaspectratio()
			self._media_control.Run()
			return True
		except COMError as e:
			print('COMError', str(e))
			self._reset()
			return False

	########################################
	#
	########################################
	def record_view_video_device_avi (self, avi_file, idx_video, idx_audio=-1):

		self._create_interfaces()
		if idx_video==INDEX_SPOUTCAM:
			self._cam, name = self._create_object_from_path(CLSID_SpoutCam, FILTER_DIR+'\\SpoutCam.ax'), 'SpoutCam'
		elif idx_video==INDEX_SCREENCAM:
			self._cam, name = self._create_object_from_path(CLSID_ScreenCam, FILTER_DIR+'\\ScreenCam.dll'), 'ScreenCam'
		else:
			self._cam, name = self._get_filter_by_index(CLSID_VideoInputDeviceCategory, idx_video)
		self._filter_graph.AddFilter(self._cam, name)

		# Find an output pin on the filter
		self._cam_pin_out = self._get_unconnected_pin(self._cam, PIN_DIR_OUT)
		if self._cam_pin_out is None:
			self._reset()
			return False

		try:
			# Tee Filter
			teeFilter = client.CreateObject(CLSID_TeeFilter, interface = IBaseFilter)
			self._filter_graph.AddFilter(teeFilter, 'Tee Filter')

			# MJPEG Compressor
			mjpegCompressor = client.CreateObject(CLSID_MJPEGCompressor, interface = IBaseFilter)
			self._filter_graph.AddFilter(mjpegCompressor, 'MJPEG Compressor')

			# AVI Muxer
			aviMuxer = client.CreateObject(CLSID_AVIMuxer, interface = IBaseFilter)
			self._filter_graph.AddFilter(aviMuxer, 'AVI Muxer')

			# File Writer
			fileWriter = client.CreateObject(CLSID_FileWriter, interface = IBaseFilter)
			self._filter_graph.AddFilter(fileWriter, 'File Writer')

			# Set dest filename
			sink = fileWriter.QueryInterface(IFileSinkFilter)
			sink.SetFileName(avi_file, None)

			# Add Video Mixing Renderer
			self._vmr9 = client.CreateObject(CLSID_VideoMixingRenderer9, interface = IBaseFilter)
			self._filter_graph.AddFilter(self._vmr9, 'Video Mixing Renderer 9')
			self._filter_config = self._vmr9.QueryInterface(IVMRFilterConfig9)
			hr = self._filter_config.SetRenderingMode(VMR9Mode_Windowless)
			self._windowless_control = self._vmr9.QueryInterface(IVMRWindowlessControl9)
			r = RECT(0, 0, int(self.width()*self._size_factor), int(self.height()*self._size_factor))
			self._windowless_control.SetVideoPosition(None, byref(r))
			self._windowless_control.SetVideoClippingWindow(self._hwnd)

			# Connect
			pin_mjpeg_in = self._get_pin_by_name(mjpegCompressor, 'Input')
			pin_mjpeg_out = self._get_pin_by_name(mjpegCompressor, 'Output')

			self._filter_graph.ConnectDirect(self._cam_pin_out, self._get_pin_by_name(teeFilter, 'Input'), None)
			pin = self._get_unconnected_pin(teeFilter, PIN_DIR_OUT)
			try:
				self._filter_graph.ConnectDirect(pin, pin_mjpeg_in, None)
			except:
				# Direct connection failed, so try intelligent connect
				self._graph_builder.Connect(pin, pin_mjpeg_in)

			self._filter_graph.ConnectDirect(pin_mjpeg_out, self._get_pin_by_name(aviMuxer, 'Input'), None)
			self._filter_graph.ConnectDirect(self._get_pin_by_name(aviMuxer, 'AVI Out'), self._get_pin_by_name(fileWriter, 'in'), None)

			# use best MJPEG quality
			try:
				# Specifies the quality as a value between 0.0 and 1.0, where 1.0 indicates the best quality
				videoCompression = pin_mjpeg_out.QueryInterface(IAMVideoCompression)
				videoCompression.put_Quality(1.0)
			except: pass

			# Render the Tee Filter's next output pin
			pin1 = self._get_unconnected_pin(teeFilter, PIN_DIR_OUT)
			pin2 = self._get_unconnected_pin(self._vmr9, PIN_DIR_IN)
			self._graph_builder.Connect(pin1, pin2)

			if idx_audio>=0:
				audio_source, name = self._get_filter_by_index(CLSID_AudioInputDeviceCategory, idx_audio)
				self._filter_graph.AddFilter(audio_source, name)
				pin_audio_out =  self._get_unconnected_pin(audio_source, PIN_DIR_OUT)
				pin_muxer_in =  self._get_unconnected_pin(aviMuxer, PIN_DIR_IN)
				try:
					self._filter_graph.ConnectDirect(pin_audio_out, pin_muxer_in, None)
				except:
					self._graph_builder.Connect(pin_audio_out, pin_muxer_in)

			self.set_keepaspectratio()
			self._media_control.Run()
			return True
		except COMError as e:
			print('COMError', str(e))
			self._reset()
			return False

	########################################
	#
	########################################
	def record_view_video_device_mp4 (self, mp4_file, idx_video, idx_audio=-1):

		self._create_interfaces()
		if idx_video==INDEX_SPOUTCAM:
			self._cam, name = self._create_object_from_path(CLSID_SpoutCam, FILTER_DIR+'\\SpoutCam.ax'), 'SpoutCam'
		elif idx_video==INDEX_SCREENCAM:
			self._cam, name = self._create_object_from_path(CLSID_ScreenCam, FILTER_DIR+'\\ScreenCam.dll'), 'ScreenCam'
		else:
			self._cam, name = self._get_filter_by_index(CLSID_VideoInputDeviceCategory, idx_video)
		self._filter_graph.AddFilter(self._cam, name)

		# Find an output pin on the filter
		self._cam_pin_out = self._get_unconnected_pin(self._cam, PIN_DIR_OUT)
		if self._cam_pin_out is None:
			self._reset()
			return False

		try:
			# Tee Filter
			teeFilter = client.CreateObject(CLSID_TeeFilter, interface = IBaseFilter)
			self._filter_graph.AddFilter(teeFilter, 'Tee Filter')

			os.chdir(FILTER_DIR)

			# CSIR VPP H264 Encoder
			CLSID_CSIRVPPH264Encoder = '{28D61FDF-2646-422D-834C-EFFF45884A36}'
			h264Encoder = self._create_object_from_path(CLSID_CSIRVPPH264Encoder, FILTER_DIR+'\\H264EncoderFilter.dll')
			self._filter_graph.AddFilter(h264Encoder, 'CSIR VPP H264 Encoder')

			# MPC Matroska Muxer
			CLSID_MPCMatroskaMuxer = '{1E1299A2-9D42-4F12-8791-D79E376F4143}'
			mp4Muxer = self._create_object_from_path(CLSID_MPCMatroskaMuxer, FILTER_DIR+'\\MatroskaMuxer.ax')
			self._filter_graph.AddFilter(mp4Muxer, 'MPC Matroska Muxer')

			# File Writer
			fileWriter = client.CreateObject(CLSID_FileWriter, interface = IBaseFilter)
			self._filter_graph.AddFilter(fileWriter, 'File Writer')

			# Set dest filename
			sink = fileWriter.QueryInterface(IFileSinkFilter)
			sink.SetFileName(mp4_file, None)

			# Add Video Mixing Renderer
			self._vmr9 = client.CreateObject(CLSID_VideoMixingRenderer9, interface = IBaseFilter)
			self._filter_graph.AddFilter(self._vmr9, 'Video Mixing Renderer 9')
			self._filter_config = self._vmr9.QueryInterface(IVMRFilterConfig9)
			hr = self._filter_config.SetRenderingMode(VMR9Mode_Windowless)
			self._windowless_control = self._vmr9.QueryInterface(IVMRWindowlessControl9)
			r = RECT(0, 0, int(self.width()*self._size_factor), int(self.height()*self._size_factor))
			self._windowless_control.SetVideoPosition(None, byref(r))
			self._windowless_control.SetVideoClippingWindow(self._hwnd)

			# Connect
			pin_h264Encoder_in = self._get_unconnected_pin(h264Encoder, PIN_DIR_IN)
			pin_h264Encoder_out = self._get_unconnected_pin(h264Encoder, PIN_DIR_OUT)

			self._filter_graph.ConnectDirect(self._cam_pin_out, self._get_pin_by_name(teeFilter, 'Input'), None)
			pin = self._get_unconnected_pin(teeFilter, PIN_DIR_OUT)
			try:
				self._filter_graph.ConnectDirect(pin, pin_h264Encoder_in, None)
			except:
				# Direct connection failed, so try intelligent connect
				self._graph_builder.Connect(pin, pin_h264Encoder_in)

			self._filter_graph.ConnectDirect(pin_h264Encoder_out, self._get_unconnected_pin(mp4Muxer, PIN_DIR_IN), None)
			self._filter_graph.ConnectDirect(self._get_unconnected_pin(mp4Muxer, PIN_DIR_OUT), self._get_pin_by_name(fileWriter, 'in'), None)

			# Render the Tee Filter's next output pin
			pin1 = self._get_unconnected_pin(teeFilter, PIN_DIR_OUT)
			pin2 = self._get_unconnected_pin(self._vmr9, PIN_DIR_IN)
			self._graph_builder.Connect(pin1, pin2)

			if idx_audio>=0:
				audio_source, name = self._get_filter_by_index(CLSID_AudioInputDeviceCategory, idx_audio)
				self._filter_graph.AddFilter(audio_source, name)
				pin_audio_out =  self._get_unconnected_pin(audio_source, PIN_DIR_OUT)
				pin_muxer_in =  self._get_unconnected_pin(mp4Muxer, PIN_DIR_IN)
				try:
					self._filter_graph.ConnectDirect(pin_audio_out, pin_muxer_in, None)
				except:
					self._graph_builder.Connect(pin_audio_out, pin_muxer_in)

			self.set_keepaspectratio()
			self._media_control.Run()
			return True
		except COMError as e:
			print('COMError', str(e))
			self._reset()
			return False

	########################################
	#
	########################################
	def close_graph (self):
		if self._media_control is not None:
			self._media_control.Stop()

		# Needed for DroidCam?
		if self._filter_graph is not None:
			enum = self._filter_graph.EnumFilters()
			while True:
				filt, fetched = enum.Next(1)
				if not fetched: break
				self._filter_graph.RemoveFilter(filt)
				enum.Reset()

		self._reset()
		self.update()

	########################################
	#
	########################################
	def pause (self):
		if self._media_control is None:
			return False
		self._media_control.Pause()
		return True

	########################################
	#
	########################################
	def play (self):
		if self._media_control is None:
			return False
		self._media_control.Run()
		return True

	########################################
	#
	########################################
	def stop (self):
		if self._media_control is None:
			return False
		self._media_control.Stop()
		self.update()
		return True

	########################################
	#
	########################################
	def get_size (self):
		if self._windowless_control is None:
			return False, 0, 0
		w,h,aw,ah = self._windowless_control.GetNativeVideoSize()
		return True, w, h

	########################################
	#
	########################################
	def get_fps (self):
		if self._cam_pin_out:
			try:
				am = self._cam_pin_out.ConnectionMediaType()
				formattype = str(am.formattype)
				if formattype == FORMAT_VideoInfo or formattype == FORMAT_MPEGVideo:
					info = cast(am.pbFormat, POINTER(VIDEOINFOHEADER))
					return round(10000000/info.contents.AvgTimePerFrame, 4)
				elif formattype == FORMAT_VideoInfo2 or formattype == FORMAT_MPEG2_VIDEO:
					info = cast(am.pbFormat, POINTER(VIDEOINFOHEADER2))
					return round(10000000/info.contents.AvgTimePerFrame, 4)
			except COMError as e:
				print('COMError', str(e))
			except:
				pass

	########################################
	# Saves as BMP
	########################################
	def take_snapshot (self, filename):
		if self._windowless_control is None:
			return False
		lpDib = self._windowless_control.GetCurrentImage()
		size = windll.kernel32.GlobalSize(lpDib)
		buf = bytes(size)
		memmove(buf, lpDib, size)
		self._save_dib(filename, buf)
		return True

	########################################
	#
	########################################
	def set_keepaspectratio (self, flag=True):
		if self._vmr9 is None:
			return False
		aspect_control = self._vmr9.QueryInterface(IVMRAspectRatioControl9)
		aspect_control.SetAspectRatioMode(VMR_ARMODE_LETTER_BOX if flag else VMR_ARMODE_NONE)
		return True

	########################################
	# The objects to be changed are provided through a previous call to IPropertyPage::SetObjects.
	# By calling IPropertyPage::SetObjects prior to calling this method, the caller ensures that all
	# underlying objects have the correct interfaces through which to communicate changes.
	# Therefore, this method should not fail because of non-existent interfaces.
	#
	# After applying its values, the property page should determine if its state is now current with
	# the objects in order to properly implement IPropertyPage::IsPageDirty and to provide both S_OK and S_FALSE return values.
	########################################
	def apply_filter_settings (self):
		hr = self._prop_page_filter.Apply()
		return hr==0

	########################################
	#
	########################################
	def apply_pin_settings (self):
		hr = self._prop_page_pin.Apply()
		return hr==0

	########################################
	# Shows a modal dialog
	########################################
	def show_filter_dialog (self, filterIndex):
		enum = self._filter_graph.EnumFilters()
		i = 0
		while True:
			filt, fetched = enum.Next(1)
			if not fetched: break
			if i==filterIndex:
				try:
					spec_pages = filt.QueryInterface(ISpecifyPropertyPages)
					cauuid = spec_pages.GetPages()
					if cauuid.element_count > 0:
						ok = False
						for i in range(cauuid.element_count):
							self.page = c_void_p(None)
							hr = windll.ole32.CoCreateInstance(byref(cauuid.elements[i]), 0, 1, byref(IPropertyPage._iid_), byref(self.page))
							if hr==0:
								ok = True
								break
						if not ok:
							windll.ole32.CoTaskMemFree(cauuid.elements)
							return False
						filterInfo = filt.QueryFilterInfo()
						filterName = ''.join(map(chr, filterInfo.achName)).rstrip('\0')
						pFilterUnk = cast(filt, LPUNKNOWN)
						try:
							hr = OleCreatePropertyFrame(
								self.winId().__int__(), # Parent window
								0, 0,				    # Reserved
								filterName,		        # Caption for the dialog box
								1,					    # number of objects
								byref(pFilterUnk),	    # Array of object pointers
								cauuid.element_count,   # Number of property pages
								cauuid.elements,	    # Array of property page CLSIDs
								0,					    # Locale identifier
								0, None			        # Reserved
							)
							ok = True
						except:
							ok = False
						# Clean up
						windll.ole32.CoTaskMemFree(cauuid.elements)
						return ok

				except COMError as e:
					#print('COMError', str(e))
					pass
				break
			i = i+1
		return False

	########################################
	# Queries the capture filter for interface ISpecifyPropertyPages
	########################################
	def show_filter_settings (self):
		try:
			spec_pages = self._cam.QueryInterface(ISpecifyPropertyPages)
			cauuid = spec_pages.GetPages()
			if cauuid.element_count > 0:
				ok = False
				for i in range(cauuid.element_count):
					if self._page:
						page = self._page
						hr = 0
					else:
						page = c_void_p(None)
						hr = windll.ole32.CoCreateInstance(byref(cauuid.elements[i]), 0, 1, byref(IPropertyPage._iid_), byref(page))
					if hr==0:
						ok = True
						break
				if not ok:
					windll.ole32.CoTaskMemFree(cauuid.elements)
					return False

				self._prop_page_filter = cast(page, POINTER(IPropertyPage))
				self._prop_obj_filter = self._cam
				hr = self._prop_page_filter.SetObjects(1, byref(self._prop_obj_filter))

				pageInfo = self._prop_page_filter.GetPageInfo()

				# Required dimensions of the page's dialog box in pixels
				self._filter_settings_container.setMinimumWidth(pageInfo.size.cx/self._size_factor)
				self._filter_settings_container.setMinimumHeight(pageInfo.size.cy/self._size_factor)

				hr = self._prop_page_filter.SetPageSite(MyPropertyPageSite())
				r = RECT(0, 0, pageInfo.size.cx, pageInfo.size.cy)
				hr = self._prop_page_filter.Activate(self._hwnd_filter_settings, byref(r), False)

				windll.ole32.CoTaskMemFree(cauuid.elements)
				return True

		except COMError as e:
			#print('COMError', str(e))
			pass

		return False

	########################################
	# Queries the capture filter's first pin for interface ISpecifyPropertyPages
	########################################
	def show_pin_settings (self):
		try:
			enum2 = self._cam.EnumPins()
			pin, fetched = enum2.Next(1)
			#if fetched:
			spec_pages = pin.QueryInterface(ISpecifyPropertyPages)
			cauuid = spec_pages.GetPages()
			if cauuid.element_count > 0:
				ok = False
				for i in range(cauuid.element_count):
					page = c_void_p(None)
					hr = windll.ole32.CoCreateInstance(byref(cauuid.elements[i]), 0, 1, byref(IPropertyPage._iid_), byref(page))
					if hr==0:
						ok = True
						break
				if not ok:
					windll.ole32.CoTaskMemFree(cauuid.elements)
					return False

				self._prop_page_pin = cast(page, POINTER(IPropertyPage))
				self._prop_obj_pin = pin
				hr = self._prop_page_pin.SetObjects(1, byref(self._prop_obj_pin))

				pageInfo = self._prop_page_pin.GetPageInfo()

				# Required dimensions of the page's dialog box in pixels
				self._pin_settings_container.setMinimumWidth(pageInfo.size.cx/self._size_factor)
				self._pin_settings_container.setMinimumHeight(pageInfo.size.cy/self._size_factor)

				hr = self._prop_page_pin.SetPageSite(MyPropertyPageSite())
				r = RECT(0, 0, pageInfo.size.cx, pageInfo.size.cy)
				hr = self._prop_page_pin.Activate(self._hwnd_pin_settings, byref(r), False)

				windll.ole32.CoTaskMemFree(cauuid.elements)
				return True

		except COMError as e:
			#print('COMError', str(e))
			pass

		return False

	########################################
	#
	########################################
	def close_filter_settings (self):
		if self._prop_obj_filter is not None:
			hr = self._prop_page_filter.SetObjects(0, byref(self._prop_obj_filter))
			self._prop_obj_filter = None
			hr = self._prop_page_filter.Deactivate()

	########################################
	#
	########################################
	def close_pin_settings (self):
		if self._prop_obj_pin is not None:
			hr = self._prop_page_pin.SetObjects(0, byref(self._prop_obj_pin))
			self._prop_obj_pin = None
			hr = self._prop_page_pin.Deactivate()

	########################################
	#
	########################################
	def get_video_input_devices (self):
		return self._get_available_filters(CLSID_VideoInputDeviceCategory)

	########################################
	#
	########################################
	def get_audio_input_devices (self):
		return self._get_available_filters(CLSID_AudioInputDeviceCategory)

	########################################
	#
	########################################
	def get_current_filters (self):
		if self._filter_graph is None:
			return False, E_NOINTERFACE
		filters = []
		enum = self._filter_graph.EnumFilters()
		while True:
			filt, fetched = enum.Next(1)
			if not fetched: break
			clsid = str(filt.GetClassID())
			filterInfo = filt.QueryFilterInfo()
			filterName = ''.join(map(chr, filterInfo.achName)).rstrip('\0')
			filters.append([clsid, filterName])
		return True, filters

	########################################
	#
	########################################
	def resizeEvent (self, e):
		self._resize(e.size().width(), e.size().height())
		super().resizeEvent(e)

	########################################
	#
	########################################
	def nativeEvent (self, eventType, message):
		if eventType == 'windows_generic_MSG':
			msg = MSG.from_address(message.__int__())
			if msg.message==WM_LBUTTONDBLCLK:
				self.mouseDoubleClicked.emit(msg.lParam & 0x0000ffff, msg.lParam >> 16)
			elif msg.message==WM_LBUTTONDOWN:
				self.mousePressed.emit(msg.lParam & 0x0000ffff, msg.lParam >> 16)
		# Return True if the event should be filtered, i.e. stopped.
		# Return False to allow normal Qt processing to continue
		return False, 0

	########################################
	#
	########################################
	def disconnect_filters (self):
		enum_filter = self._filter_graph.EnumFilters()
		while True:
			filt, fetched = enum_filter.Next(1)
			if not fetched: break
			try:
				pin_out, pin_in = self._get_connected_pins(filt)
				self._filter_graph.Disconnect(pin_out)
				self._filter_graph.Disconnect(pin_in)
			except:
				pass

	########################################
	#
	########################################
	def reconnect_filters (self):
		# Just render the output pin again
		self._graph_builder.Render(self._cam_pin_out)
		self.set_keepaspectratio()
		self._media_control.Run()
