from ctypes import (
		POINTER, windll, sizeof, c_int, c_long, c_longlong, c_ulonglong)
from ctypes.wintypes import (
		WORD, DWORD, ULONG, HWND, UINT, LPCOLESTR, LCID, LPVOID, INT, BOOL, FLOAT, DOUBLE, 
		COLORREF, HDC, RECT, LONG, LPBYTE, LPWSTR, MSG, LPOLESTR, SIZE, BYTE)
from comtypes import (
		IUnknown, Structure, GUID, COMMETHOD, HRESULT, BSTR, dispid)
from comtypes.automation import IDispatch

LONG_PTR = c_longlong
REFERENCE_TIME = c_longlong
DWORDLONG = c_ulonglong

class AM_MEDIA_TYPE(Structure):
	_fields_ = (
		('majortype', GUID),
		('subtype', GUID),
		('bFixedSizeSamples', BOOL),
		('bTemporalCompression', BOOL),
		('lSampleSize', ULONG),
		('formattype', GUID),
		('pUnk', POINTER(IUnknown)),
		('cbFormat', ULONG),
		('pbFormat', LPBYTE)
	)

class BITMAPINFOHEADER(Structure):
	_fields_ = (
		('biSize', DWORD),
		('biWidth', LONG),
		('biHeight', LONG),
		('biPlanes', WORD),
		('biBitCount', WORD),
		('biCompression', DWORD),
		('biSizeImage', DWORD),
		('biXPelsPerMeter', LONG),
		('biYPelsPerMeter', LONG),
		('biClrUsed', DWORD),
		('biClrImportant', DWORD)
	)

class VIDEOINFOHEADER(Structure):
	_fields_ = (
		('rcSource', RECT),
		('rcTarget', RECT),
		('dwBitRate', DWORD),
		('dwBitErrorRate', DWORD),
		('AvgTimePerFrame', REFERENCE_TIME),
		('bmiHeader', BITMAPINFOHEADER)
	)

class VIDEOINFOHEADER2(Structure):
	_fields_ = (
		('rcSource', RECT),
		('rcTarget', RECT),
		('dwBitRate', DWORD),
		('dwBitErrorRate', DWORD),
		('AvgTimePerFrame', REFERENCE_TIME),
		('dwInterlaceFlags', DWORD),
		('dwCopyProtectFlags', DWORD),
		('dwPictAspectRatioX', DWORD),
		('dwPictAspectRatioY', DWORD),
		('dwControlFlags', DWORD),
		('dwReserved2', DWORD),
		('bmiHeader', BITMAPINFOHEADER)
	)

########################################
# IBasicAudio
########################################
#class IBasicAudio(IDispatch):
#	_case_insensitive_ = True
#	'IBasicAudio interface'
#	_iid_ = GUID('{56A868B3-0AD4-11CE-B03A-0020AF0BA770}')
#	_idlflags_ = ['dual', 'oleautomation']
#	
#IBasicAudio._methods_ = [
#	COMMETHOD([dispid(1610743808), 'propput'], HRESULT, 'Volume',
#			  ( ['in'], c_int, 'plVolume' )),
#	COMMETHOD([dispid(1610743808), 'propget'], HRESULT, 'Volume',
#			  ( ['out', 'retval'], POINTER(c_int), 'plVolume' )),
#	COMMETHOD([dispid(1610743810), 'propput'], HRESULT, 'Balance',
#			  ( ['in'], c_int, 'plBalance' )),
#	COMMETHOD([dispid(1610743810), 'propget'], HRESULT, 'Balance',
#			  ( ['out', 'retval'], POINTER(c_int), 'plBalance' )),
#]

########################################
# IMediaControl
########################################
class IMediaControl(IDispatch):
	_case_insensitive_ = True
	'IMediaControl interface'
	_iid_ = GUID('{56A868B1-0AD4-11CE-B03A-0020AF0BA770}')
	_idlflags_ = ['dual', 'oleautomation']

IMediaControl._methods_ = [
	COMMETHOD([dispid(1610743808)], HRESULT, 'Run'),
	COMMETHOD([dispid(1610743809)], HRESULT, 'Pause'),
	COMMETHOD([dispid(1610743810)], HRESULT, 'Stop'),
	COMMETHOD([dispid(1610743811)], HRESULT, 'GetState',
			  ( ['in'], c_int, 'msTimeout' ),
			  ( ['out'], POINTER(c_int), 'pfs' )),
	COMMETHOD([dispid(1610743812)], HRESULT, 'RenderFile',
			  ( ['in'], BSTR, 'strFilename' )),
	COMMETHOD([dispid(1610743813)], HRESULT, 'AddSourceFilter',
			  ( ['in'], BSTR, 'strFilename' ),
			  ( ['out'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
	COMMETHOD([dispid(1610743814), 'propget'], HRESULT, 'FilterCollection',
			  ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
	COMMETHOD([dispid(1610743815), 'propget'], HRESULT, 'RegFilterCollection',
			  ( ['out', 'retval'], POINTER(POINTER(IDispatch)), 'ppUnk' )),
	COMMETHOD([dispid(1610743816)], HRESULT, 'StopWhenReady'),
]

########################################
# IMediaEvent
########################################
#class IMediaEvent(IDispatch):
#	_case_insensitive_ = True
#	'IMediaEvent interface'
#	_iid_ = GUID('{56A868B6-0AD4-11CE-B03A-0020AF0BA770}')
#	_idlflags_ = ['dual', 'oleautomation']
#
#IMediaEvent._methods_ = [
#	COMMETHOD([dispid(1610743808)], HRESULT, 'GetEventHandle',
#			  ( ['out'], POINTER(LONG_PTR), 'hEvent' )),
#	COMMETHOD([dispid(1610743809)], HRESULT, 'GetEvent',
#			  ( ['out'], POINTER(c_int), 'lEventCode' ),
#			  ( ['out'], POINTER(LONG_PTR), 'lParam1' ),
#			  ( ['out'], POINTER(LONG_PTR), 'lParam2' ),
#			  ( ['in'], c_int, 'msTimeout' )),
#	COMMETHOD([dispid(1610743810)], HRESULT, 'WaitForCompletion',
#			  ( ['in'], c_int, 'msTimeout' ),
#			  ( ['out'], POINTER(c_int), 'pEvCode' )),
#	COMMETHOD([dispid(1610743811)], HRESULT, 'CancelDefaultHandling',
#			  ( ['in'], c_int, 'lEvCode' )),
#	COMMETHOD([dispid(1610743812)], HRESULT, 'RestoreDefaultHandling',
#			  ( ['in'], c_int, 'lEvCode' )),
#	COMMETHOD([dispid(1610743813)], HRESULT, 'FreeEventParams',
#			  ( ['in'], c_int, 'lEvCode' ),
#			  ( ['in'], LONG_PTR, 'lParam1' ),
#			  ( ['in'], LONG_PTR, 'lParam2' )),
#]

########################################
# IMediaEventEx
########################################
#class IMediaEventEx(IMediaEvent):
#	_case_insensitive_ = True
#	'IMediaEventEx interface'
#	_iid_ = GUID('{56A868C0-0AD4-11CE-B03A-0020AF0BA770}')
#	_idlflags_ = []
#
#IMediaEventEx._methods_ = [
#	COMMETHOD([], HRESULT, 'SetNotifyWindow',
#			  ( ['in'], LONG_PTR, 'hwnd' ),
#			  ( ['in'], c_int, 'lMsg' ),
#			  ( ['in'], LONG_PTR, 'lInstanceData' )),
#	COMMETHOD([], HRESULT, 'SetNotifyFlags',
#			  ( ['in'], c_int, 'lNoNotifyFlags' )),
#	COMMETHOD([], HRESULT, 'GetNotifyFlags',
#			  ( ['out'], POINTER(c_int), 'lplNoNotifyFlags' )),
#]

########################################
# OleCreatePropertyFrame
########################################
LPUNKNOWN = POINTER(IUnknown)
CLSID = GUID
LPCLSID = POINTER(CLSID)

OleCreatePropertyFrame = windll.oleaut32.OleCreatePropertyFrame
OleCreatePropertyFrame.restype = HRESULT
OleCreatePropertyFrame.argtypes = (
	HWND,  # [in] hwndOwner
	UINT,  # [in] x
	UINT,  # [in] y
	LPCOLESTR,  # [in] lpszCaption
	ULONG,  # [in] cObjects
	POINTER(LPUNKNOWN),  # [in] ppUnk
	ULONG,  # [in] cPages
	LPCLSID,  # [in] pPageClsID
	LCID,  # [in] lcid
	DWORD,  # [in] dwReserved
	LPVOID,  # [in] pvReserved
)

########################################
# ISpecifyPropertyPages
########################################
class ISpecifyPropertyPages(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{B196B28B-BAB4-101A-B69C-00AA00341D07}')
	_idlflags_ = []
	
class CAUUID(Structure):
	_fields_ = (
		('element_count', ULONG),
		('elements', POINTER(GUID)),
	)

ISpecifyPropertyPages._methods_ = [
	COMMETHOD([], HRESULT, 'GetPages',
			(['out'], POINTER(CAUUID), 'pPages'))
]

########################################
# IPropertyPageSite
########################################
class IPropertyPageSite(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{B196B28C-BAB4-101A-B69C-00AA00341D07}')
	_idlflags_ = []
	
IPropertyPageSite._methods_ = [
	COMMETHOD([], HRESULT, 'OnStatusChange',
			(['in'], DWORD, 'dwFlags')),
	COMMETHOD([], HRESULT, 'GetLocaleID',
			(['out'], POINTER(LCID), 'pLocaleID')),
	COMMETHOD([], HRESULT, 'GetPageContainer',
			(['out'], POINTER(POINTER(IUnknown)), 'ppUnk')),
	COMMETHOD([], HRESULT, 'TranslateAccelerator',
			(['in'], POINTER(MSG), 'pMsg'))
]

########################################
# IPropertyPage
########################################
class IPropertyPage(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{B196B28D-BAB4-101A-B69C-00AA00341D07}')
	_idlflags_ = []
    
class PROPPAGEINFO(Structure):
	_fields_ = (
		('cb', ULONG),
		('pszTitle', LPOLESTR),
		('size', SIZE),
		('pszDocString', LPOLESTR),
		('pszHelpFile', LPOLESTR),
		('dwHelpContext', DWORD),
	)
	
IPropertyPage._methods_ = [
	COMMETHOD([], HRESULT, 'SetPageSite',
			(['in'], POINTER(IPropertyPageSite), 'pPageSite')),
	COMMETHOD([], HRESULT, 'Activate',
			(['in'], HWND, 'hWndParent'),
			(['in'], POINTER(RECT), 'pRect'),
			(['in'], BOOL, 'bModal')),
	COMMETHOD([], HRESULT, 'Deactivate'),
	COMMETHOD([], HRESULT, 'GetPageInfo',
			(['out'], POINTER(PROPPAGEINFO), 'pPageInfo')),
	COMMETHOD([], HRESULT, 'SetObjects',
			(['in'], ULONG, 'cObjects'),
			(['size_is', 'in'], POINTER(POINTER(IUnknown)), 'ppUnk')),
	COMMETHOD([], HRESULT, 'Show',
			(['in'], UINT, 'nCmdShow')),
	COMMETHOD([], HRESULT, 'Move',
			(['in'], POINTER(RECT), 'pRect')),
	COMMETHOD([], HRESULT, 'IsPageDirty'),
	COMMETHOD([], HRESULT, 'Apply'),
	COMMETHOD([], HRESULT, 'Help',
			(['in'], LPCOLESTR, 'pszHelpDir')),
	COMMETHOD([], HRESULT, 'TranslateAccelerator',
			(['in'], POINTER(MSG), 'pMsg'))
]      

########################################
# IAMMediaContent
########################################
#class IAMMediaContent(IDispatch):
#	_case_insensitive_ = True
#	_iid_ = GUID('{FA2AA8F4-8B62-11D0-A520-000000000000}')
#	_idlflags_ = []
#	
#IAMMediaContent._methods_ = [
#	COMMETHOD([], HRESULT, 'get_AuthorName',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrAuthorName')),
#	COMMETHOD([], HRESULT, 'get_Title',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrTitle')),
#	COMMETHOD([], HRESULT, 'get_Rating',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrRating')),
#	COMMETHOD([], HRESULT, 'get_Description',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrDescription')),
#	COMMETHOD([], HRESULT, 'get_Copyright',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrCopyright')),		
#	COMMETHOD([], HRESULT, 'get_BaseURL',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrBaseURL')),
#	COMMETHOD([], HRESULT, 'get_LogoURL',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrLogoURL')),
#	COMMETHOD([], HRESULT, 'get_LogoIconURL',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrLogoURL')),
#	COMMETHOD([], HRESULT, 'get_WatermarkURL',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrWatermarkURL')),
#	COMMETHOD([], HRESULT, 'get_MoreInfoURL',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrMoreInfoURL')),
#	COMMETHOD([], HRESULT, 'get_MoreInfoBannerImage',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrMoreInfoBannerImage')),
#	COMMETHOD([], HRESULT, 'get_MoreInfoBannerURL',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrMoreInfoBannerURL')),
#	COMMETHOD([], HRESULT, 'get_MoreInfoText',
#			(['retval', 'out'], POINTER(BSTR), 'pbstrMoreInfoText'))
#]

########################################
# IAMStreamSelect
########################################
#class IAMStreamSelect(IUnknown):
#	_case_insensitive_ = True
#	_iid_ = GUID('{C1960960-17F5-11D1-ABE1-00A0C905F375}')
#	_idlflags_ = []
#
#IAMStreamSelect._methods_ = [
#	COMMETHOD([], HRESULT, 'Count',
#			(['out'], POINTER(DWORD), 'pcStreams')),
#	COMMETHOD([], HRESULT, 'Info',
#			(['in'], LONG, 'lIndex'),
#			(['annotation', 'out'], POINTER(POINTER(AM_MEDIA_TYPE)), 'ppmt'),
#			(['annotation', 'out'], POINTER(DWORD), 'pdwFlags'),
#			(['annotation', 'out'], POINTER(LCID), 'plcid'),
#			(['annotation', 'out'], POINTER(DWORD), 'pdwGroup'),
#			(['annotation', 'out'], POINTER(LPWSTR), 'ppszName'),
#			(['annotation', 'out'], POINTER(POINTER(IUnknown)), 'ppObject'),
#			(['annotation', 'out'], POINTER(POINTER(IUnknown)), 'ppUnk')),
#	COMMETHOD([], HRESULT, 'Enable',
#			(['in'], LONG, 'lIndex'),
#			(['in'], DWORD, 'dwFlags'))
#]

########################################
# IAMVideoCompression
########################################
#class IAMVideoCompression(IUnknown):
#	_case_insensitive_ = True
#	_iid_ = GUID('{C6E13343-30AC-11d0-A18C-00A0C9118956}')
#	_idlflags_ = []
#	
#IAMVideoCompression._methods_ = [
#	COMMETHOD([], HRESULT, 'put_KeyFrameRate',
#			(['in'], LONG, 'KeyFrameRate')),
#	COMMETHOD([], HRESULT, 'get_KeyFrameRate',
#			(['out'], POINTER(LONG), 'pKeyFrameRate')),
#	COMMETHOD([], HRESULT, 'put_PFramesPerKeyFrame',
#			(['in'], LONG, 'PFramesPerKeyFrame')),
#	COMMETHOD([], HRESULT, 'get_PFramesPerKeyFrame',
#			(['out'], POINTER(LONG), 'pPFramesPerKeyFrame')),
#	COMMETHOD([], HRESULT, 'put_Quality',
#			(['in'], DOUBLE, 'Quality')),
#	COMMETHOD([], HRESULT, 'get_Quality',
#			(['out'], POINTER(DOUBLE), 'pQuality')),
#	COMMETHOD([], HRESULT, 'put_WindowSize',
#			(['in'], DWORDLONG, 'WindowSize')),
#	COMMETHOD([], HRESULT, 'get_WindowSize',
#			(['out'], POINTER(DWORDLONG), 'pWindowSize')),			
#	COMMETHOD([], HRESULT, 'GetInfo',
#			(['in'], LPWSTR, 'pszVersion'),
#			(['in'], POINTER(INT), 'pcbVersion'),
#			(['in'], LPWSTR, 'pszDescription'),
#			(['in'], POINTER(INT), 'pcbDescription'),
#			(['in'], POINTER(LONG), 'pDefaultKeyFrameRate'),
#			(['in'], POINTER(LONG), 'pDefaultPFramesPerKey'),
#			(['in'], POINTER(DOUBLE), 'pDefaultQuality'),
#			(['in'], POINTER(LONG), 'pCapabilities')),
#	COMMETHOD([], HRESULT, 'OverrideKeyFrame',
#			(['in'], LONG, 'FrameNumber')),
#	COMMETHOD([], HRESULT, 'OverrideFrameSize',
#			(['in'], LONG, 'FrameNumber'),
#			(['in'], LONG, 'Size'))
#]
            
########################################
# IAMStreamConfig
########################################
#class IAMStreamConfig(IUnknown):
#	_case_insensitive_ = True
#	_iid_ = GUID('{C6E13340-30AC-11d0-A18C-00A0C9118956}')
#	_idlflags_ = []
#
#IAMStreamConfig._methods_ = [
#	COMMETHOD([], HRESULT, 'SetFormat',
#			(['in'], POINTER(AM_MEDIA_TYPE), 'pmt')),
#	COMMETHOD([], HRESULT, 'GetFormat',
#			(['annotation', 'out'], POINTER(POINTER(AM_MEDIA_TYPE)), 'ppmt')),
#					
#	COMMETHOD([], HRESULT, 'GetNumberOfCapabilities',
#			(['annotation', 'out'], POINTER(c_int), 'piCount'),
#			(['annotation', 'out'], POINTER(c_int), 'piSize')),
#	COMMETHOD([], HRESULT, 'GetStreamCaps',
#			(['in'], c_int, 'iIndex'),
#			(['annotation', 'out'], POINTER(AM_MEDIA_TYPE), 'ppmt'),
#			(['annotation', 'out'], POINTER(BYTE), 'pSCC'))
#]

########################################
# IAMVfwCaptureDialogs
########################################
#class IAMVfwCaptureDialogs(IUnknown):
#	_case_insensitive_ = True
#	_iid_ = GUID('{D8D715A0-6E5E-11D0-B3F0-00AA003761C5}')
#	_idlflags_ = []
#
#IAMStreamConfig._methods_ = [
#	COMMETHOD([], HRESULT, 'HasDialog',
#			(['in'], c_int, 'iDialog')),
#	COMMETHOD([], HRESULT, 'ShowDialog',
#			(['in'], c_int, 'iDialog'),	
#			(['in'], HWND, 'hwnd')),	
#	COMMETHOD([], HRESULT, 'SendDriverMessage',
#			(['in'], c_int, 'iDialog'),	
#			(['in'], c_int, 'uMsg'),	
#			(['in'], c_long, 'dw1'),	
#			(['in'], c_long, 'dw2'))
#]
