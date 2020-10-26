from ctypes import (
		POINTER, windll, sizeof)
	
from ctypes.wintypes import (
		DWORD, ULONG, HWND, UINT, LPCOLESTR, LCID, LPVOID, HDC, INT, BOOL, FLOAT, COLORREF, RECT, LPRECT, LONG, BYTE, LPBYTE)

from comtypes import (
		IUnknown, Structure, GUID, COMMETHOD, HRESULT, BSTR)

from comtypes.automation import IDispatch

from videowidget.d3d import *

VMR9Mode_Windowless	= 0x2

VMR9AlphaBitmap_Disable = 1
VMR9AlphaBitmap_EntireDDS = 4

VMR9ARMode_None = 0
VMR9ARMode_LetterBox = 1

########################################
# Structures
########################################

class VMR9ProcAmpControl(Structure):
	_fields_ = (
		('dwSize', DWORD),
		('dwFlags', DWORD),
		('Brightness', FLOAT),
		('Contrast', FLOAT),
		('Hue', FLOAT),
		('Saturation', FLOAT)
	)
	def __init__(self):
		self.dwSize = sizeof(self)

class VMR9ProcAmpControlRange(Structure):
	_fields_ = (
		('dwSize', DWORD),
		('dwProperty', DWORD),
		('MinValue', FLOAT),
		('MaxValue', FLOAT),
		('DefaultValue', FLOAT),
		('StepSize', FLOAT)
	)
	def __init__(self):
		self.dwSize = sizeof(self)

class VMR9NormalizedRect(Structure):
	_fields_ = (
		('left', FLOAT),
		('top', FLOAT),
		('right', FLOAT),
		('bottom', FLOAT)
	)
	
class VMR9AlphaBitmap(Structure):
	_fields_ = (
		('dwFlags', DWORD),
		('hdc', HDC),
		('pDDS', POINTER(IDirect3DSurface9)),
		('rSrc', RECT),
		('rDest', VMR9NormalizedRect),
		('fAlpha', FLOAT),
		('clrSrcKey', COLORREF),
		('dwFilterMode', DWORD)
	)

########################################
# IVMRAspectRatioControl9
########################################
class IVMRAspectRatioControl9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{00D96C29-BBDE-4EFC-9901-BB5036392146}')
	_idlflags_ = []
	
IVMRAspectRatioControl9._methods_ = [
	COMMETHOD([], HRESULT, 'GetAspectRatioMode',
			(['retval', 'out'], POINTER(DWORD), 'lpdwARMode')),
	COMMETHOD([], HRESULT, 'SetAspectRatioMode',
			(['in'], DWORD, 'dwARMode')),
			]

########################################
# IVMRMixerControl9
# https://msdn.microsoft.com/en-us/windows/desktop/dd390457
########################################
class IVMRMixerControl9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{1A777EAA-47C8-4930-B2C9-8FEE1C1B0F3B}')
	_idlflags_ = []

IVMRMixerControl9._methods_ = [
	COMMETHOD([], HRESULT, 'SetAlpha',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], FLOAT, 'Alpha')),
	COMMETHOD([], HRESULT, 'GetAlpha',
			(['in'], DWORD, 'dwStreamID'),
			(['out'], POINTER(FLOAT), 'pAlpha')),
	COMMETHOD([], HRESULT, 'SetZOrder',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], DWORD, 'dwZ')),
	COMMETHOD([], HRESULT, 'GetZOrder',
			(['in'], DWORD, 'dwStreamID'),
			(['out'], POINTER(DWORD), 'pZ')),
	COMMETHOD([], HRESULT, 'SetOutputRect',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], POINTER(VMR9NormalizedRect), 'pRect')),
	COMMETHOD([], HRESULT, 'GetOutputRect',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], POINTER(VMR9NormalizedRect), 'pRect')),
	COMMETHOD([], HRESULT, 'SetBackgroundClr',
			(['in'], COLORREF, 'ClrBkg')),
	COMMETHOD([], HRESULT, 'GetBackgroundClr',
			(['in'], POINTER(COLORREF), 'lpClrBkg')),
	COMMETHOD([], HRESULT, 'SetMixingPrefs',
			(['in'], DWORD, 'dwMixerPrefs')),
	COMMETHOD([], HRESULT, 'GetMixingPrefs',
			(['out'], POINTER(DWORD), 'pdwMixerPrefs')),
	COMMETHOD([], HRESULT, 'SetProcAmpControl',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], POINTER(VMR9ProcAmpControl), 'lpClrControl')),
	COMMETHOD([], HRESULT, 'GetProcAmpControl',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], POINTER(VMR9ProcAmpControl), 'lpClrControl')),
	COMMETHOD([], HRESULT, 'GetProcAmpControlRange',
			(['in'], DWORD, 'dwStreamID'),
			(['in'], POINTER(VMR9ProcAmpControlRange), 'lpClrControl'))
		]

########################################
# IVMRImageCompositor9
########################################
class IVMRImageCompositor9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{4A5C89EB-DF51-4654-AC2A-E48E02BBABF6}')
	_idlflags_ = []
	
IVMRImageCompositor9._methods_ = [
	COMMETHOD([], HRESULT, 'InitCompositionDevice',
			(['in'], POINTER(IUnknown), 'pD3DDevice')),
		]

#        virtual HRESULT STDMETHODCALLTYPE TermCompositionDevice( 
#            /* [in] */ IUnknown *pD3DDevice) = 0;
#        
#        virtual HRESULT STDMETHODCALLTYPE SetStreamMediaType( 
#            /* [in] */ DWORD dwStrmID,
#            /* [in] */ AM_MEDIA_TYPE *pmt,
#            /* [in] */ BOOL fTexture) = 0;
#        
#        virtual HRESULT STDMETHODCALLTYPE CompositeImage( 
#            /* [in] */ IUnknown *pD3DDevice,
#            /* [in] */ IDirect3DSurface9 *pddsRenderTarget,
#            /* [in] */ AM_MEDIA_TYPE *pmtRenderTarget,
#            /* [in] */ REFERENCE_TIME rtStart,
#            /* [in] */ REFERENCE_TIME rtEnd,
#            /* [in] */ D3DCOLOR dwClrBkGnd,
#            /* [in] */ VMR9VideoStreamInfo *pVideoStreamInfo,
#            /* [in] */ UINT cStreams) = 0;
#        
#    };
    
########################################
# IVMRFilterConfig9
########################################
class IVMRFilterConfig9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{5A804648-4F66-4867-9C43-4F5C822CF1B8}')
	_idlflags_ = []
	
IVMRFilterConfig9._methods_ = [
	COMMETHOD([], HRESULT, 'SetImageCompositor',
			(['in'], POINTER(IVMRImageCompositor9), 'lpVMRImgCompositor')),
	COMMETHOD([], HRESULT, 'SetNumberOfStreams',
			(['in'], DWORD, 'dwMaxStreams')),
	COMMETHOD([], HRESULT, 'GetNumberOfStreams',
			(['out'], POINTER(DWORD), 'pdwMaxStreams')),
	COMMETHOD([], HRESULT, 'SetRenderingPrefs',
			(['in'], DWORD, 'dwRenderFlags')),
	COMMETHOD([], HRESULT, 'GetRenderingPrefs',
			(['out'], POINTER(DWORD), 'pdwRenderFlags')),
	COMMETHOD([], HRESULT, 'SetRenderingMode',
			(['in'], DWORD, 'Mode')),
	COMMETHOD([], HRESULT, 'GetRenderingMode',
			(['out'], POINTER(DWORD), 'pMode')),
		]

########################################
# IVMRWindowlessControl9
########################################
class IVMRWindowlessControl9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{8F537D09-F85E-4414-B23B-502E54C79927}')
	_idlflags_ = []
	
IVMRWindowlessControl9._methods_ = [
	COMMETHOD([], HRESULT, 'GetNativeVideoSize',
			(['out'], POINTER(LONG), 'lpWidth'),
			(['out'], POINTER(LONG), 'lpHeight'),
			(['out'], POINTER(LONG), 'lpARWidth'),
			(['out'], POINTER(LONG), 'lpARHeight')),
	COMMETHOD([], HRESULT, 'GetMinIdealVideoSize',
			(['out'], POINTER(LONG), 'lpWidth'),
			(['out'], POINTER(LONG), 'lpHeight')),
	COMMETHOD([], HRESULT, 'GetMaxIdealVideoSize',
			(['out'], POINTER(LONG), 'lpWidth'),
			(['out'], POINTER(LONG), 'lpHeight')),	
	COMMETHOD([], HRESULT, 'SetVideoPosition',
			(['in'], LPRECT, 'lpSRCRect'),
			(['in'], LPRECT, 'lpDSTRect')),
	COMMETHOD([], HRESULT, 'GetVideoPosition',
			(['out'], LPRECT, 'lpSRCRect'),
			(['out'], LPRECT, 'lpDSTRect')),
	COMMETHOD([], HRESULT, 'GetAspectRatioMode',
			(['out'], POINTER(DWORD), 'lpAspectRatioMode')),
	COMMETHOD([], HRESULT, 'SetAspectRatioMode',
			(['in'], DWORD, 'AspectRatioMode')),
	COMMETHOD([], HRESULT, 'SetVideoClippingWindow',
			(['in'], HWND, 'hwnd')),
	COMMETHOD([], HRESULT, 'RepaintVideo',
			(['in'], HWND, 'hwnd'),
			(['in'], HDC, 'hdc')),
	COMMETHOD([], HRESULT, 'DisplayModeChanged',
			),
	COMMETHOD([], HRESULT, 'GetCurrentImage',
			#(['out'], POINTER(LPBYTE), 'lpDib'))
			(['out'], POINTER(POINTER(BYTE)), 'lpDib'))
		]

#virtual HRESULT STDMETHODCALLTYPE SetBorderColor( 
#    /* [in] */ COLORREF Clr) = 0;
#
#virtual HRESULT STDMETHODCALLTYPE GetBorderColor( 
#    /* [out] */ COLORREF *lpClr) = 0;

########################################
# IVMRMixerBitmap9
########################################
class IVMRMixerBitmap9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{CED175E5-1935-4820-81BD-FF6AD00C9108}')
	_idlflags_ = []

IVMRMixerBitmap9._methods_ = [
	COMMETHOD([], HRESULT, 'SetAlphaBitmap',
			(['in'], POINTER(VMR9AlphaBitmap), 'pBmpParms')),
	COMMETHOD([], HRESULT, 'UpdateAlphaBitmapParameters',
			(['in'], POINTER(VMR9AlphaBitmap), 'pBmpParms')),	
	COMMETHOD([], HRESULT, 'GetAlphaBitmapParameters',
			(['out'], POINTER(VMR9AlphaBitmap), 'pBmpParms')),
			]
