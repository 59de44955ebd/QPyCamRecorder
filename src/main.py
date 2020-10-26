# ****************************************************************************
# @file QPyCamViewer - main class
# @author Valentin Schmidt
# @version 0.3
# ****************************************************************************

import os
import sys
import time
import traceback

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5 import uic

from videowidget import INDEX_SPOUTCAM, INDEX_SCREENCAM

APP_NAME = 'QPyCamRecorder'
APP_VERSION = 3

LOAD_LOCAL_SCREENCAM = True
LOAD_LOCAL_SPOUTCAM = True

PATH = os.path.dirname(os.path.realpath(__file__))

########################################
#
########################################
class Main (QMainWindow):

	########################################
	# @constructor
	########################################
	def __init__ (self):
		super().__init__()

		# load UI
		QResource.registerResource(PATH+'\\resources\\main.rcc')
		uic.loadUi(PATH+'\\resources\\main.ui', self)

		devices = self.videowidget.get_video_input_devices()
		i = 0
		for d in devices:
			action = QAction(self.menuDevices)
			action.setText(d)
			action.setData(i)
			action.setShortcut('Ctrl+'+str(i))
			action.triggered.connect(self.slot_open_device)
			self.menuDevices.addAction(action)
			i = i+1

		self.menuDevices.addSeparator()

		if LOAD_LOCAL_SPOUTCAM and not 'SpoutCam' in devices:
			#self.menuDevices.addSeparator()
			action = QAction(self.menuDevices)
			action.setText('SpoutCam (internal)')
			action.setData(INDEX_SPOUTCAM)
			action.setShortcut('Ctrl+'+str(i))
			action.triggered.connect(self.slot_open_device)
			self.menuDevices.addAction(action)

		if LOAD_LOCAL_SCREENCAM and not 'ScreenCam' in devices:
			action = QAction(self.menuDevices)
			action.setText('ScreenCam (internal)')
			action.setData(INDEX_SCREENCAM)
			action.setShortcut('Ctrl+'+str(i))
			action.triggered.connect(self.slot_open_device)
			self.menuDevices.addAction(action)

		# audio
		self._actionGroupAudioSource = QActionGroup(self)
		self._actionGroupAudioSource.addAction(self.actionAudioNone)
		self.actionAudioNone.setData(-1)
		devices = self.videowidget.get_audio_input_devices()
		i = 0
		for d in devices:
			action = QAction(self.menuRecordAudio)
			action.setText(d)
			action.setData(i)
			action.setCheckable(True)
			self.menuRecordAudio.addAction(action)
			self._actionGroupAudioSource.addAction(action)
			i = i+1

		self.actionClose.triggered.connect(self.slot_close_device)
		self.actionSaveImage.triggered.connect(self.slot_take_snapshot)

		ag = QActionGroup(self)
		ag.addAction(self.actionAVI)
		ag.addAction(self.actionMP4)

		self.menuFilters.triggered.connect(self.slot_menu_filters_triggered)
		self.actionAbout.triggered.connect(self.slot_about)

		self.setup_button_bar()

		self._current_device_idx = None
		self._current_device_name = None

		self._is_recording = False

		self.videowidget.set_filter_settings_container(self.containerFilterSettings)
		self.buttonBoxFilter.clicked.connect(self.slot_apply_filter_settings)

		self.videowidget.set_pin_settings_container(self.containerPinSettings)
		self.buttonBoxPin.clicked.connect(self.slot_apply_pin_settings)

		self.videowidget.mouseDoubleClicked.connect(self.slot_toogle_fullscreen)

		self.widgetPanels.hide()

		self.resize(1000, 600)
		self.show()

	########################################
	# Shows status info in status bar
	########################################
	def msg (self, s, ms=5000):
		self.statusbar.showMessage(s, ms)

	########################################
	# Shows error message in status bar
	########################################
	def err (self, s):
		self.statusbar.showMessage('Error: '+s)

	########################################
	#
	########################################
	def setup_button_bar (self):
		self._buttonBar = QToolBar(self)
		self._buttonBar.setObjectName('buttonbar')
		self._buttonBar.setWindowTitle('ButtonBar')
		self._buttonBar.setIconSize(QSize(16, 16))
		self._buttonBar.setFloatable(False)
		self._buttonBar.setMovable(False)

		self._buttonBar.layout().setSpacing(4)

		self._playButton = QToolButton(self._buttonBar)
		self._playButton.setToolTip('Play')
		self._playButton.setIcon(QIcon(':/icons/play.png'))
		self._playButton.setCheckable(True)
		self._playButton.clicked.connect(self.slot_play)
		self._buttonBar.addWidget(self._playButton)

		self._recordButton = QToolButton(self._buttonBar)
		self._recordButton.setToolTip('Record to AVI or MP4')
		self._recordButton.setIcon(QIcon(':/icons/record.png'))
		self._recordButton.setCheckable(True)
		self._recordButton.clicked.connect(self.slot_record)
		self._buttonBar.addWidget(self._recordButton)

		self._stopButton = QToolButton(self._buttonBar)
		self._stopButton.setToolTip('Stop')
		self._stopButton.setIcon(QIcon(':/icons/stop.png'))
		self._stopButton.clicked.connect(self.slot_stop)
		self._buttonBar.addWidget(self._stopButton)

		self._buttonBar.setDisabled(True)
		self.addToolBar(Qt.BottomToolBarArea, self._buttonBar)

	########################################
	#
	########################################
	def open_device (self, device_idx, device_name):
		self.close_device()

		ok = self.videowidget.load_video_device(device_idx)
		if ok:
			self._current_device_idx = device_idx
			self._current_device_name = device_name
			self._playButton.setChecked(True)
			self.update_ui(True)
		else:
			self.update_ui(False)

	########################################
	#
	########################################
	def close_device (self):
		self.videowidget.close_filter_settings()
		self.videowidget.close_pin_settings()
		self.videowidget.close_graph()

		self._current_device_idx = None
		self._current_device_name = None

		self._playButton.setChecked(False)
		self._recordButton.setChecked(False)

		self.update_ui(False)

	########################################
	#
	########################################
	def record_device (self, video_device_idx, video_device_name):
		self.close_device()

		recDir = PATH+'\\..\\recordings\\'
		if not os.path.isdir(recDir): os.mkdir(recDir)
		video_file = os.path.abspath(recDir + video_device_name)

		audio_device_idx = self._actionGroupAudioSource.checkedAction().data()

		if self.actionMP4.isChecked():
			video_file += '_'+time.strftime('%Y%m%d_%H%M%S')+'.mp4'
			if self.actionDisplayWhileRecording.isChecked():
				ok = self.videowidget.record_view_video_device_mp4(video_file, video_device_idx, audio_device_idx)
			else:
				ok = self.videowidget.record_video_device_mp4(video_file, video_device_idx, audio_device_idx)
		else:
			video_file += '_'+time.strftime('%Y%m%d_%H%M%S')+'.avi'
			if self.actionDisplayWhileRecording.isChecked():
				ok = self.videowidget.record_view_video_device_avi(video_file, video_device_idx, audio_device_idx)
			else:
				ok = self.videowidget.record_video_device_avi(video_file, video_device_idx, audio_device_idx)

		if ok:
			self.msg('Recording to '+video_file+' ...', 0)
			self._current_device_idx = video_device_idx
			self._current_device_name = video_device_name
			self.update_ui(True)
		else:
			self.err('Recording failed')
			self.update_ui(False)

		self._is_recording = ok

	########################################
	#
	########################################
	def update_ui (self, device_loaded):
		self.actionClose.setEnabled(device_loaded)
		self.actionSaveImage.setEnabled(device_loaded)

		self._buttonBar.setEnabled(device_loaded)

		# update filter menu
		self.menuFilters.clear()
		if device_loaded:
			ok, filters = self.videowidget.get_current_filters()
			if not ok: return
			i = 0
			filters.reverse()
			for f in filters:
				filtername = f[1]
				action = QAction(self.menuFilters)
				action.setText(filtername)
				action.setData(len(filters)-i-1)
				self.menuFilters.addAction(action)
				i = i+1

			# update infos
			self.labelDevice.setText(self._current_device_name)
			ok, w, h = self.videowidget.get_size()
			self.labelResolution.setText(str(w)+' x '+str(h) if ok else '')
			fps = self.videowidget.get_fps()
			self.labelFps.setText('{:.2f}'.format(fps) if fps is not None else '')

			# show filter settings panel
			ok = self.videowidget.show_filter_settings()
			self.filterSettings.setVisible(ok)

			# show pin settings panel
			ok = self.videowidget.show_pin_settings()
			self.pinSettings.setVisible(ok)

			self.widgetPanels.show()

			self.setWindowTitle(self._current_device_name +' - '+APP_NAME)

		else:
			self.widgetPanels.hide()
			self.setWindowTitle(APP_NAME)

	########################################
	#
	########################################
	def slot_play (self, flag):
		if flag:
			if self._is_recording:
				self._playButton.setChecked(False) # ignore
			else:
				self.videowidget.play()
		else:
			self._playButton.setChecked(True)

	########################################
	#
	########################################
	def slot_record (self, flag):
		if flag:
			self.record_device(self._current_device_idx, self._current_device_name)
			if self._is_recording:
				self._recordButton.setChecked(True)
				self.buttonBoxFilter.setDisabled(True)
				self.buttonBoxPin.setDisabled(True)
		else:
			self._recordButton.setChecked(True)

	########################################
	#
	########################################
	def slot_stop (self):
		if self._current_device_idx is None: return
		if self._is_recording:
			self.msg('Recording finished.')
			self._is_recording = False
			self.open_device(self._current_device_idx, self._current_device_name)
			self._recordButton.setChecked(False)
			self.buttonBoxFilter.setDisabled(False)
			self.buttonBoxPin.setDisabled(False)
		else:
			self.videowidget.stop()
			self._playButton.setChecked(False)

	########################################
	# @callback
	########################################
	def slot_open_device (self):
		device_idx = self.sender().data()
		device_name = self.sender().text()
		self.open_device(device_idx, device_name)

	########################################
	# @callback
	########################################
	def slot_close_device (self):
		self.slot_stop()
		self.close_device()

	########################################
	#
	########################################
	def slot_apply_filter_settings (self, btn):
		self.videowidget.stop()

		self.videowidget.disconnect_filters()

		self.videowidget.apply_filter_settings()

		# rebuild graph
		#self.open_device(self._current_device_idx, self._current_device_name)

		#self.videowidget.play()

		self.videowidget.reconnect_filters()

		# update infos
		ok, w, h = self.videowidget.get_size()
		self.labelResolution.setText(str(w)+' x '+str(h) if ok else '')

		fps = self.videowidget.get_fps()
		self.labelFps.setText('{:.2f}'.format(fps) if fps is not None else '')

	########################################
	#
	########################################
	def slot_apply_pin_settings (self, btn):
		self.videowidget.stop()
		self.videowidget.apply_pin_settings()
		self.videowidget.play()

		# update infos
		ok, w, h = self.videowidget.get_size()
		self.labelResolution.setText(str(w)+' x '+str(h) if ok else '')
		fps = self.videowidget.get_fps()
		self.labelFps.setText('{:.2f}'.format(fps) if fps is not None else '')

	########################################
	#
	########################################
	def slot_toogle_fullscreen (self):
		if self.videowidget.isFullScreen():
			self.setCentralWidget(self.videowidget)
			self.videowidget.setGeometry(self._geo)
		else:
			self._geo = self.videowidget.geometry()
			self.videowidget.setParent(None)
			self.videowidget.showFullScreen()
			self.videowidget._resize(self.videowidget.width(), self.videowidget.height())

	########################################
	# @callback
	########################################
	def slot_take_snapshot (self):
		snapshotDir = PATH+'\\..\\snapshots\\'
		if not os.path.isdir(snapshotDir): os.mkdir(snapshotDir)
		fn = os.path.abspath(snapshotDir + self._current_device_name)
		fn += '_'+time.strftime('%Y%m%d_%H%M%S')+'.bmp'
		ok = self.videowidget.take_snapshot(fn)
		if ok:
			self.msg('Snapshot saved as '+fn)
		else:
			self.err('Failed to save snapshot')

	########################################
	# @callback
	########################################
	def slot_menu_filters_triggered (self, action):
		ok = self.videowidget.show_filter_dialog(action.data())

	########################################
	# @callback
	########################################
	def slot_about (self):
		msg = '<b>'+APP_NAME+' v0.'+str(APP_VERSION)+'</b><br>(c) 2020 Valentin Schmidt<br><br>'+\
				'A simple Camera Viewer and Recorder based on <br>Python 3, PyQt5 and DirectShow.'
		QMessageBox.about(self, 'About '+APP_NAME, msg)

########################################
#
########################################
if __name__ == '__main__':
	if os.path.basename(sys.executable)=='python.exe':
		sys.excepthook = traceback.print_exception
	else:
		sys.frozen = 'windows_exe'
		def excepthook(etype, e, tb):
			QMessageBox.critical(None, 'Uncaught Exception', '\n'.join(traceback.format_exception(etype, e, tb)))
		sys.excepthook = excepthook
	qApp.setAttribute(Qt.AA_EnableHighDpiScaling, True)
	app = QApplication(sys.argv)
	os.environ['PYTHONPATH'] = PATH
	main = Main()
	sys.exit(app.exec_())
