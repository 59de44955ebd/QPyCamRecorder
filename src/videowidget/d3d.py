from ctypes import *

from ctypes.wintypes import (
		DWORD, ULONG, HWND, UINT, LPCOLESTR, LCID, LPVOID, INT, BOOL, FLOAT, COLORREF, HMONITOR, HANDLE, RECT, HDC, CHAR)

from comtypes import (
		IUnknown, Structure, GUID, COMMETHOD, HRESULT)

########################################
# Constants
########################################

D3D_SDK_VERSION  = 31 | 0x80000000

D3DFMT_A8R8G8B8 = 21
D3DPOOL_SYSTEMMEM = 2
		
D3DADAPTER_DEFAULT = 0
D3DSWAPEFFECT_DISCARD = 1
D3DDEVTYPE_HAL = 1
D3DCREATE_SOFTWARE_VERTEXPROCESSING = 0x00000020

########################################
# Types
########################################

D3DFORMAT = UINT
D3DADAPTER_IDENTIFIER9 = UINT
D3DMULTISAMPLE_TYPE = UINT
D3DSWAPEFFECT = UINT
REFGUID = GUID
REFIID = GUID
D3DPOOL = UINT
D3DDEVTYPE = UINT
D3DRESOURCETYPE = UINT

########################################
# Structures
########################################

class D3DDISPLAYMODE(Structure):
	_fields_ = (
		('Width', UINT),
		('Height', UINT),
		('RefreshRate', UINT),
		('Format', D3DFORMAT)
	)


class D3DPRESENT_PARAMETERS(Structure):
	_fields_ = (
		('BackBufferWidth', UINT),
		('BackBufferHeight', UINT),
		('BackBufferFormat', D3DFORMAT),
		('BackBufferCount', UINT),
		
		('MultiSampleType', D3DMULTISAMPLE_TYPE),
		('MultiSampleQuality', DWORD),
		
		('SwapEffect', D3DSWAPEFFECT),
		('hDeviceWindow', HWND),
		
		('Windowed', BOOL),
		('EnableAutoDepthStencil', BOOL),
		('AutoDepthStencilFormat', D3DFORMAT),
		('Flags', DWORD),
		
		('FullScreen_RefreshRateInHz', UINT),
		('PresentationInterval', UINT)
	)


#/* Structure for LockRect */
#typedef struct _D3DLOCKED_RECT
#{
#    INT                 Pitch;
#    void*               pBits;
#} D3DLOCKED_RECT;
class D3DLOCKED_RECT(Structure):
	_fields_ = (
		('Pitch', INT),
		('pBits', LPVOID)
		#('pBits', c_void_p)
		#('pBits', POINTER(CHAR))
	)


#/* Surface Description */
#typedef struct _D3DSURFACE_DESC
#{
#    D3DFORMAT           Format;
#    D3DRESOURCETYPE     Type;
#    DWORD               Usage;
#    D3DPOOL             Pool;
#
#    D3DMULTISAMPLE_TYPE MultiSampleType;
#    DWORD               MultiSampleQuality;
#    UINT                Width;
#    UINT                Height;
#} D3DSURFACE_DESC;
class D3DSURFACE_DESC(Structure):
	_fields_ = (
		('Format', D3DFORMAT),
		('Type', D3DRESOURCETYPE),
		('Usage', DWORD),
		('Pool', D3DPOOL),
		
		('MultiSampleType', D3DMULTISAMPLE_TYPE),
		('MultiSampleQuality', DWORD),
		('Width', UINT),
		('Height', UINT),
	)


#typedef struct _D3DCAPS9
#{
#    /* Device Info */
#    D3DDEVTYPE  DeviceType;
#    UINT        AdapterOrdinal;
#
#    /* Caps from DX7 Draw */
#    DWORD   Caps;
#    DWORD   Caps2;
#    DWORD   Caps3;
#    DWORD   PresentationIntervals;
#
#    /* Cursor Caps */
#    DWORD   CursorCaps;
#
#    /* 3D Device Caps */
#    DWORD   DevCaps;
#
#    DWORD   PrimitiveMiscCaps;
#    DWORD   RasterCaps;
#    DWORD   ZCmpCaps;
#    DWORD   SrcBlendCaps;
#    DWORD   DestBlendCaps;
#    DWORD   AlphaCmpCaps;
#    DWORD   ShadeCaps;
#    DWORD   TextureCaps;
#    DWORD   TextureFilterCaps;          // D3DPTFILTERCAPS for IDirect3DTexture9's
#    DWORD   CubeTextureFilterCaps;      // D3DPTFILTERCAPS for IDirect3DCubeTexture9's
#    DWORD   VolumeTextureFilterCaps;    // D3DPTFILTERCAPS for IDirect3DVolumeTexture9's
#    DWORD   TextureAddressCaps;         // D3DPTADDRESSCAPS for IDirect3DTexture9's
#    DWORD   VolumeTextureAddressCaps;   // D3DPTADDRESSCAPS for IDirect3DVolumeTexture9's
#
#    DWORD   LineCaps;                   // D3DLINECAPS
#
#    DWORD   MaxTextureWidth, MaxTextureHeight;
#    DWORD   MaxVolumeExtent;
#
#    DWORD   MaxTextureRepeat;
#    DWORD   MaxTextureAspectRatio;
#    DWORD   MaxAnisotropy;
#    float   MaxVertexW;
#
#    float   GuardBandLeft;
#    float   GuardBandTop;
#    float   GuardBandRight;
#    float   GuardBandBottom;
#
#    float   ExtentsAdjust;
#    DWORD   StencilCaps;
#
#    DWORD   FVFCaps;
#    DWORD   TextureOpCaps;
#    DWORD   MaxTextureBlendStages;
#    DWORD   MaxSimultaneousTextures;
#
#    DWORD   VertexProcessingCaps;
#    DWORD   MaxActiveLights;
#    DWORD   MaxUserClipPlanes;
#    DWORD   MaxVertexBlendMatrices;
#    DWORD   MaxVertexBlendMatrixIndex;
#
#    float   MaxPointSize;
#
#    DWORD   MaxPrimitiveCount;          // max number of primitives per DrawPrimitive call
#    DWORD   MaxVertexIndex;
#    DWORD   MaxStreams;
#    DWORD   MaxStreamStride;            // max stride for SetStreamSource
#
#    DWORD   VertexShaderVersion;
#    DWORD   MaxVertexShaderConst;       // number of vertex shader constant registers
#
#    DWORD   PixelShaderVersion;
#    float   PixelShader1xMaxValue;      // max value storable in registers of ps.1.x shaders
#
#    // Here are the DX9 specific ones
#    DWORD   DevCaps2;
#
#    float   MaxNpatchTessellationLevel;
#    DWORD   Reserved5;
#
#    UINT    MasterAdapterOrdinal;       // ordinal of master adaptor for adapter group
#    UINT    AdapterOrdinalInGroup;      // ordinal inside the adapter group
#    UINT    NumberOfAdaptersInGroup;    // number of adapters in this adapter group (only if master)
#    DWORD   DeclTypes;                  // Data types, supported in vertex declarations
#    DWORD   NumSimultaneousRTs;         // Will be at least 1
#    DWORD   StretchRectFilterCaps;      // Filter caps supported by StretchRect
#    D3DVSHADERCAPS2_0 VS20Caps;
#    D3DPSHADERCAPS2_0 PS20Caps;
#    DWORD   VertexTextureFilterCaps;    // D3DPTFILTERCAPS for IDirect3DTexture9's for texture, used in vertex shaders
#    DWORD   MaxVShaderInstructionsExecuted; // maximum number of vertex shader instructions that can be executed
#    DWORD   MaxPShaderInstructionsExecuted; // maximum number of pixel shader instructions that can be executed
#    DWORD   MaxVertexShader30InstructionSlots; 
#    DWORD   MaxPixelShader30InstructionSlots;
#} D3DCAPS9;
# TODO
class D3DCAPS9(Structure):
	_fields_ = (
		('DeviceType', D3DDEVTYPE),
		)

#/* Creation Parameters */
#typedef struct _D3DDEVICE_CREATION_PARAMETERS
#{
#    UINT            AdapterOrdinal;
#    D3DDEVTYPE      DeviceType;
#    HWND            hFocusWindow;
#    DWORD           BehaviorFlags;
#} D3DDEVICE_CREATION_PARAMETERS;
class D3DDEVICE_CREATION_PARAMETERS(Structure):
	_fields_ = (
		('AdapterOrdinal', UINT),
		('DeviceType', D3DDEVTYPE),
		('hFocusWindow', HWND),
		('BehaviorFlags', DWORD),
		)


########################################
# IDirect3D9
# https://docs.microsoft.com/en-us/windows/win32/api/d3d9/nn-d3d9-idirect3d9
########################################
class IDirect3D9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{81BDCBCA-64D4-426d-AE8D-AD0147F4275C}')
	_idlflags_ = []

########################################
# IDirect3DDevice9
########################################
class IDirect3DDevice9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{D0223B96-BF7A-43fd-92BD-A43B0D82B9EB}')
	_idlflags_ = []

########################################
# IDirect3DResource9
########################################
class IDirect3DResource9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{05EEC05D-8F7D-4362-B999-D1BAF357C704}')
	_idlflags_ = []

########################################
# IDirect3DSurface9
########################################
class IDirect3DSurface9(IDirect3DResource9):
	_case_insensitive_ = True
	_iid_ = GUID('{0CFBAF3A-9FF6-429a-99B3-A2796AF8B89B}')
	_idlflags_ = []
	
	
	
	
	
	
	
#DECLARE_INTERFACE_(IDirect3DResource9, IUnknown)
#{
#    /*** IUnknown methods ***/
#    STDMETHOD(QueryInterface)(THIS_ REFIID riid, void** ppvObj) PURE;
#    STDMETHOD_(ULONG,AddRef)(THIS) PURE;
#    STDMETHOD_(ULONG,Release)(THIS) PURE;
#
#    /*** IDirect3DResource9 methods ***/
#    STDMETHOD(GetDevice)(THIS_ IDirect3DDevice9** ppDevice) PURE;
#    STDMETHOD(SetPrivateData)(THIS_ REFGUID refguid,CONST void* pData,DWORD SizeOfData,DWORD Flags) PURE;
#    STDMETHOD(GetPrivateData)(THIS_ REFGUID refguid,void* pData,DWORD* pSizeOfData) PURE;
#    STDMETHOD(FreePrivateData)(THIS_ REFGUID refguid) PURE;
#    STDMETHOD_(DWORD, SetPriority)(THIS_ DWORD PriorityNew) PURE;
#    STDMETHOD_(DWORD, GetPriority)(THIS) PURE;
#    STDMETHOD_(void, PreLoad)(THIS) PURE;
#    STDMETHOD_(D3DRESOURCETYPE, GetType)(THIS) PURE;
#};

IDirect3DResource9._methods_ = [

	#STDMETHOD(GetDevice)(THIS_ IDirect3DDevice9** ppDevice) PURE;
	COMMETHOD([], HRESULT, 'GetDevice',
			(['out'], POINTER(POINTER(IDirect3DDevice9)), 'ppDevice')),
			
	#STDMETHOD(SetPrivateData)(THIS_ REFGUID refguid,CONST void* pData,DWORD SizeOfData,DWORD Flags) PURE;
	COMMETHOD([], HRESULT, 'SetPrivateData',
			(['in'], REFGUID, 'refguid'),
			(['in'], LPVOID, 'pData'),
			(['in'], DWORD, 'SizeOfData'),
			(['in'], DWORD, 'Flags')),
			
    #STDMETHOD(GetPrivateData)(THIS_ REFGUID refguid,void* pData,DWORD* pSizeOfData) PURE;
	COMMETHOD([], HRESULT, 'GetPrivateData',
			(['in'], REFGUID, 'refguid'),
			(['in'], LPVOID, 'pData'),
			(['in'], POINTER(DWORD), 'pSizeOfData')),
			
    #STDMETHOD(FreePrivateData)(THIS_ REFGUID refguid) PURE;
	COMMETHOD([], HRESULT, 'FreePrivateData',
			(['in'], REFGUID, 'refguid')),
			
    #STDMETHOD_(DWORD, SetPriority)(THIS_ DWORD PriorityNew) PURE;
	COMMETHOD([], HRESULT, 'SetPriority',
			(['in'], DWORD, 'PriorityNew')),
			
    #STDMETHOD_(DWORD, GetPriority)(THIS) PURE;
	COMMETHOD([], DWORD, 'GetPriority',
			),
			
    #STDMETHOD_(void, PreLoad)(THIS) PURE;
	COMMETHOD([], None, 'PreLoad',
			),
			
    #STDMETHOD_(D3DRESOURCETYPE, GetType)(THIS) PURE;
	COMMETHOD([], D3DRESOURCETYPE, 'GetType',
			),	
			
		]
		
########################################
# IDirect3DSurface9
########################################
IDirect3DSurface9._methods_ = [

#    STDMETHOD(GetContainer)(THIS_ REFIID riid,void** ppContainer) PURE;
	COMMETHOD([], HRESULT, 'GetDesc',
			(['in'], REFIID, 'riid'),
			(['out'], POINTER(LPVOID), 'ppContainer')),
			
#    STDMETHOD(GetDesc)(THIS_ D3DSURFACE_DESC *pDesc) PURE;
	COMMETHOD([], HRESULT, 'GetDesc',
			(['in'], POINTER(D3DSURFACE_DESC), 'pDesc')),
			
#    STDMETHOD(LockRect)(THIS_ D3DLOCKED_RECT* pLockedRect,CONST RECT* pRect,DWORD Flags) PURE;
	COMMETHOD([], HRESULT, 'LockRect',
			(['in'], POINTER(D3DLOCKED_RECT), 'pLockedRect'),
			(['in'], POINTER(RECT), 'pLockedRect'),
			(['in'], DWORD, 'Flags')),
			
#    STDMETHOD(UnlockRect)(THIS) PURE;
	COMMETHOD([], HRESULT, 'UnlockRect',
			),

#    STDMETHOD(GetDC)(THIS_ HDC *phdc) PURE;
	COMMETHOD([], HRESULT, 'GetDC',
			(['in'], POINTER(HDC), 'phdc')),
			
#    STDMETHOD(ReleaseDC)(THIS_ HDC hdc) PURE;
	COMMETHOD([], HRESULT, 'ReleaseDC',
			(['in'], HDC, 'hdc'))
		]
		
		
#DECLARE_INTERFACE_(IDirect3DSurface9, IDirect3DResource9)
#{
#    /*** IUnknown methods ***/
#    STDMETHOD(QueryInterface)(THIS_ REFIID riid, void** ppvObj) PURE;
#    STDMETHOD_(ULONG,AddRef)(THIS) PURE;
#    STDMETHOD_(ULONG,Release)(THIS) PURE;
#
#    /*** IDirect3DResource9 methods ***/
#    STDMETHOD(GetDevice)(THIS_ IDirect3DDevice9** ppDevice) PURE;
#    STDMETHOD(SetPrivateData)(THIS_ REFGUID refguid,CONST void* pData,DWORD SizeOfData,DWORD Flags) PURE;
#    STDMETHOD(GetPrivateData)(THIS_ REFGUID refguid,void* pData,DWORD* pSizeOfData) PURE;
#    STDMETHOD(FreePrivateData)(THIS_ REFGUID refguid) PURE;
#    STDMETHOD_(DWORD, SetPriority)(THIS_ DWORD PriorityNew) PURE;
#    STDMETHOD_(DWORD, GetPriority)(THIS) PURE;
#    STDMETHOD_(void, PreLoad)(THIS) PURE;
#    STDMETHOD_(D3DRESOURCETYPE, GetType)(THIS) PURE;

#    STDMETHOD(GetContainer)(THIS_ REFIID riid,void** ppContainer) PURE;
#    STDMETHOD(GetDesc)(THIS_ D3DSURFACE_DESC *pDesc) PURE;
#    STDMETHOD(LockRect)(THIS_ D3DLOCKED_RECT* pLockedRect,CONST RECT* pRect,DWORD Flags) PURE;
#    STDMETHOD(UnlockRect)(THIS) PURE;
#    STDMETHOD(GetDC)(THIS_ HDC *phdc) PURE;
#    STDMETHOD(ReleaseDC)(THIS_ HDC hdc) PURE;
#
#    /*** Helper information ***/
#    LPCWSTR Name;
#    UINT Width;
#    UINT Height;
#    DWORD Usage;
#    D3DFORMAT Format;
#    D3DPOOL Pool;
#    D3DMULTISAMPLE_TYPE MultiSampleType;
#    DWORD MultiSampleQuality;
#    DWORD Priority;
#    UINT LockCount;
#    UINT DCCount;
#};


########################################
# IDirect3DSurface9
########################################
class IDirect3DSwapChain9(IUnknown):
	_case_insensitive_ = True
	_iid_ = GUID('{794950F2-ADFC-458a-905E-10A10B0B503B}')
	_idlflags_ = []


IDirect3DSwapChain9._methods_ = [
		]
		
#DECLARE_INTERFACE_(IDirect3DSwapChain9, IUnknown)
#{
#    /*** IUnknown methods ***/
#    STDMETHOD(QueryInterface)(THIS_ REFIID riid, void** ppvObj) PURE;
#    STDMETHOD_(ULONG,AddRef)(THIS) PURE;
#    STDMETHOD_(ULONG,Release)(THIS) PURE;
#
#    /*** IDirect3DSwapChain9 methods ***/
#    STDMETHOD(Present)(THIS_ CONST RECT* pSourceRect,CONST RECT* pDestRect,HWND hDestWindowOverride,CONST RGNDATA* pDirtyRegion,DWORD dwFlags) PURE;
#    STDMETHOD(GetFrontBufferData)(THIS_ IDirect3DSurface9* pDestSurface) PURE;
#    STDMETHOD(GetBackBuffer)(THIS_ UINT iBackBuffer,D3DBACKBUFFER_TYPE Type,IDirect3DSurface9** ppBackBuffer) PURE;
#    STDMETHOD(GetRasterStatus)(THIS_ D3DRASTER_STATUS* pRasterStatus) PURE;
#    STDMETHOD(GetDisplayMode)(THIS_ D3DDISPLAYMODE* pMode) PURE;
#    STDMETHOD(GetDevice)(THIS_ IDirect3DDevice9** ppDevice) PURE;
#    STDMETHOD(GetPresentParameters)(THIS_ D3DPRESENT_PARAMETERS* pPresentationParameters) PURE;
#
#    /*** Helper information ***/
#    D3DPRESENT_PARAMETERS PresentParameters;
#    D3DDISPLAYMODE DisplayMode;
#};





########################################
# IDirect3DDevice9
########################################
IDirect3DDevice9._methods_ = [
	#STDMETHOD(TestCooperativeLevel)(THIS) PURE;
	COMMETHOD([], HRESULT, 'TestCooperativeLevel',
			),
			
	#STDMETHOD_(UINT, GetAvailableTextureMem)(THIS) PURE;
	COMMETHOD([], UINT, 'GetAvailableTextureMem',
			),
			
	#STDMETHOD(EvictManagedResources)(THIS) PURE;
	COMMETHOD([], HRESULT, 'EvictManagedResources',
			),
	
	#STDMETHOD(GetDirect3D)(THIS_ IDirect3D9** ppD3D9) PURE;
	COMMETHOD([], HRESULT, 'GetDirect3D',
			(['out'], POINTER(POINTER(IDirect3D9)), 'ppD3D9')),
			
	#STDMETHOD(GetDeviceCaps)(THIS_ D3DCAPS9* pCaps) PURE;
	COMMETHOD([], HRESULT, 'GetDeviceCaps',
			(['out'], POINTER(D3DCAPS9), 'pCaps')),
	
	#STDMETHOD(GetDisplayMode)(THIS_ UINT iSwapChain,D3DDISPLAYMODE* pMode) PURE;
	COMMETHOD([], HRESULT, 'GetDisplayMode',
			(['in'], UINT, 'iSwapChain'),
			(['out'], POINTER(D3DDISPLAYMODE), 'pMode')),
			
	#STDMETHOD(GetCreationParameters)(THIS_ D3DDEVICE_CREATION_PARAMETERS *pParameters) PURE;
	COMMETHOD([], HRESULT, 'GetCreationParameters',
			(['out'], POINTER(D3DDEVICE_CREATION_PARAMETERS), 'pParameters')),
		
	#STDMETHOD(SetCursorProperties)(THIS_ UINT XHotSpot,UINT YHotSpot,IDirect3DSurface9* pCursorBitmap) PURE;
	COMMETHOD([], HRESULT, 'SetCursorProperties',
			(['in'], UINT, 'XHotSpot'),
			(['in'], UINT, 'YHotSpot'),
			(['in'], POINTER(IDirect3DSurface9), 'pCursorBitmap')),
			
	#STDMETHOD_(void, SetCursorPosition)(THIS_ int X,int Y,DWORD Flags) PURE;
	COMMETHOD([], HRESULT, 'SetCursorPosition',
			(['in'], INT, 'X'),
			(['in'], INT, 'Y'),
			(['in'], DWORD, 'Flags')),
			
	#STDMETHOD_(BOOL, ShowCursor)(THIS_ BOOL bShow) PURE;
	COMMETHOD([], BOOL, 'ShowCursor',
			(['in'], BOOL, 'bShow')),
			
	#STDMETHOD(CreateAdditionalSwapChain)(THIS_ D3DPRESENT_PARAMETERS* pPresentationParameters,IDirect3DSwapChain9** pSwapChain) PURE;
	COMMETHOD([], HRESULT, 'CreateAdditionalSwapChain',
			(['in'], POINTER(D3DPRESENT_PARAMETERS), 'pPresentationParameters'),
			(['out'], POINTER(IDirect3DSwapChain9), 'pSwapChain')),
			
	#STDMETHOD(GetSwapChain)(THIS_ UINT iSwapChain,IDirect3DSwapChain9** pSwapChain) PURE;
	COMMETHOD([], HRESULT, 'GetSwapChain',
			(['in'], UINT, 'iSwapChain'),
			(['out'], POINTER(IDirect3DSwapChain9), 'pSwapChain')),	
			
	#STDMETHOD_(UINT, GetNumberOfSwapChains)(THIS) PURE;
	COMMETHOD([], UINT, 'GetNumberOfSwapChains',
			),
			
	#STDMETHOD(Reset)(THIS_ D3DPRESENT_PARAMETERS* pPresentationParameters) PURE;	
	COMMETHOD([], HRESULT, 'Reset',
			(['in'], POINTER(D3DPRESENT_PARAMETERS), 'pPresentationParameters')),
			
	#STDMETHOD(Present)(THIS_ CONST RECT* pSourceRect,CONST RECT* pDestRect,HWND hDestWindowOverride,CONST RGNDATA* pDirtyRegion) PURE;
	COMMETHOD([], HRESULT, 'Present',
			),
			
	#STDMETHOD(GetBackBuffer)(THIS_ UINT iSwapChain,UINT iBackBuffer,D3DBACKBUFFER_TYPE Type,IDirect3DSurface9** ppBackBuffer) PURE;
	COMMETHOD([], HRESULT, 'GetBackBuffer',
			),
			
	#STDMETHOD(GetRasterStatus)(THIS_ UINT iSwapChain,D3DRASTER_STATUS* pRasterStatus) PURE;
	COMMETHOD([], HRESULT, 'GetRasterStatus',
			),
			
	#STDMETHOD(SetDialogBoxMode)(THIS_ BOOL bEnableDialogs) PURE;
	COMMETHOD([], HRESULT, 'SetDialogBoxMode',
			),
			
	#STDMETHOD_(void, SetGammaRamp)(THIS_ UINT iSwapChain,DWORD Flags,CONST D3DGAMMARAMP* pRamp) PURE;
	COMMETHOD([], HRESULT, 'SetGammaRamp',
			),
			
	#STDMETHOD_(void, GetGammaRamp)(THIS_ UINT iSwapChain,D3DGAMMARAMP* pRamp) PURE;
	COMMETHOD([], HRESULT, 'GetGammaRamp',
			),
			
	#STDMETHOD(CreateTexture)(THIS_ UINT Width,UINT Height,UINT Levels,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DTexture9** ppTexture,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateTexture',
			),
			
	#STDMETHOD(CreateVolumeTexture)(THIS_ UINT Width,UINT Height,UINT Depth,UINT Levels,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DVolumeTexture9** ppVolumeTexture,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateVolumeTexture',
			),
				
	#STDMETHOD(CreateCubeTexture)(THIS_ UINT EdgeLength,UINT Levels,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DCubeTexture9** ppCubeTexture,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateCubeTexture',
			),
				
	#STDMETHOD(CreateVertexBuffer)(THIS_ UINT Length,DWORD Usage,DWORD FVF,D3DPOOL Pool,IDirect3DVertexBuffer9** ppVertexBuffer,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateVertexBuffer',
			),
				
	#STDMETHOD(CreateIndexBuffer)(THIS_ UINT Length,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DIndexBuffer9** ppIndexBuffer,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateIndexBuffer',
			),
				
	#STDMETHOD(CreateRenderTarget)(THIS_ UINT Width,UINT Height,D3DFORMAT Format,D3DMULTISAMPLE_TYPE MultiSample,DWORD MultisampleQuality,BOOL Lockable,IDirect3DSurface9** ppSurface,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateRenderTarget',
			),
				
	#STDMETHOD(CreateDepthStencilSurface)(THIS_ UINT Width,UINT Height,D3DFORMAT Format,D3DMULTISAMPLE_TYPE MultiSample,DWORD MultisampleQuality,BOOL Discard,IDirect3DSurface9** ppSurface,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateDepthStencilSurface',
			),
				
	#STDMETHOD(UpdateSurface)(THIS_ IDirect3DSurface9* pSourceSurface,CONST RECT* pSourceRect,IDirect3DSurface9* pDestinationSurface,CONST POINT* pDestPoint) PURE;
	COMMETHOD([], HRESULT, 'UpdateSurface',
			),
				
	#STDMETHOD(UpdateTexture)(THIS_ IDirect3DBaseTexture9* pSourceTexture,IDirect3DBaseTexture9* pDestinationTexture) PURE;
	COMMETHOD([], HRESULT, 'UpdateTexture',
			),
				
	#STDMETHOD(GetRenderTargetData)(THIS_ IDirect3DSurface9* pRenderTarget,IDirect3DSurface9* pDestSurface) PURE;
	COMMETHOD([], HRESULT, 'GetRenderTargetData',
			),
				
	#STDMETHOD(GetFrontBufferData)(THIS_ UINT iSwapChain,IDirect3DSurface9* pDestSurface) PURE;
	COMMETHOD([], HRESULT, 'GetFrontBufferData',
			),
				
	#STDMETHOD(StretchRect)(THIS_ IDirect3DSurface9* pSourceSurface,CONST RECT* pSourceRect,IDirect3DSurface9* pDestSurface,CONST RECT* pDestRect,D3DTEXTUREFILTERTYPE Filter) PURE;
	COMMETHOD([], HRESULT, 'StretchRect',
			),
				
	#STDMETHOD(ColorFill)(THIS_ IDirect3DSurface9* pSurface,CONST RECT* pRect,D3DCOLOR color) PURE;
	COMMETHOD([], HRESULT, 'ColorFill',
			),

	#STDMETHOD(CreateOffscreenPlainSurface)(THIS_ UINT Width,UINT Height,D3DFORMAT Format,D3DPOOL Pool,IDirect3DSurface9** ppSurface,HANDLE* pSharedHandle) PURE;
	COMMETHOD([], HRESULT, 'CreateOffscreenPlainSurface',
			(['in'], UINT, 'Width'),
			(['in'], UINT, 'Height'),
			(['in'], D3DFORMAT, 'Format'),
			(['in'], D3DPOOL, 'Pool'),
			(['out'], POINTER(POINTER(IDirect3DSurface9)), 'ppSurface'),
			(['in'], POINTER(HANDLE), 'pSharedHandle')),
		]
    
#/*** IDirect3DDevice9 methods ***/
	#STDMETHOD(TestCooperativeLevel)(THIS) PURE;
	#STDMETHOD_(UINT, GetAvailableTextureMem)(THIS) PURE;
	#STDMETHOD(EvictManagedResources)(THIS) PURE;
	#STDMETHOD(GetDirect3D)(THIS_ IDirect3D9** ppD3D9) PURE;
	#STDMETHOD(GetDeviceCaps)(THIS_ D3DCAPS9* pCaps) PURE;
	#STDMETHOD(GetDisplayMode)(THIS_ UINT iSwapChain,D3DDISPLAYMODE* pMode) PURE;
	#STDMETHOD(GetCreationParameters)(THIS_ D3DDEVICE_CREATION_PARAMETERS *pParameters) PURE;
	#STDMETHOD(SetCursorProperties)(THIS_ UINT XHotSpot,UINT YHotSpot,IDirect3DSurface9* pCursorBitmap) PURE;
	#STDMETHOD_(void, SetCursorPosition)(THIS_ int X,int Y,DWORD Flags) PURE;
	#STDMETHOD_(BOOL, ShowCursor)(THIS_ BOOL bShow) PURE;
	#STDMETHOD(CreateAdditionalSwapChain)(THIS_ D3DPRESENT_PARAMETERS* pPresentationParameters,IDirect3DSwapChain9** pSwapChain) PURE;
	#STDMETHOD(GetSwapChain)(THIS_ UINT iSwapChain,IDirect3DSwapChain9** pSwapChain) PURE;
	#STDMETHOD_(UINT, GetNumberOfSwapChains)(THIS) PURE;
	#STDMETHOD(Reset)(THIS_ D3DPRESENT_PARAMETERS* pPresentationParameters) PURE;
	#STDMETHOD(Present)(THIS_ CONST RECT* pSourceRect,CONST RECT* pDestRect,HWND hDestWindowOverride,CONST RGNDATA* pDirtyRegion) PURE;
	#STDMETHOD(GetBackBuffer)(THIS_ UINT iSwapChain,UINT iBackBuffer,D3DBACKBUFFER_TYPE Type,IDirect3DSurface9** ppBackBuffer) PURE;
	#STDMETHOD(GetRasterStatus)(THIS_ UINT iSwapChain,D3DRASTER_STATUS* pRasterStatus) PURE;
	#STDMETHOD(SetDialogBoxMode)(THIS_ BOOL bEnableDialogs) PURE;
	#STDMETHOD_(void, SetGammaRamp)(THIS_ UINT iSwapChain,DWORD Flags,CONST D3DGAMMARAMP* pRamp) PURE;
	#STDMETHOD_(void, GetGammaRamp)(THIS_ UINT iSwapChain,D3DGAMMARAMP* pRamp) PURE;
	#STDMETHOD(CreateTexture)(THIS_ UINT Width,UINT Height,UINT Levels,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DTexture9** ppTexture,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(CreateVolumeTexture)(THIS_ UINT Width,UINT Height,UINT Depth,UINT Levels,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DVolumeTexture9** ppVolumeTexture,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(CreateCubeTexture)(THIS_ UINT EdgeLength,UINT Levels,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DCubeTexture9** ppCubeTexture,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(CreateVertexBuffer)(THIS_ UINT Length,DWORD Usage,DWORD FVF,D3DPOOL Pool,IDirect3DVertexBuffer9** ppVertexBuffer,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(CreateIndexBuffer)(THIS_ UINT Length,DWORD Usage,D3DFORMAT Format,D3DPOOL Pool,IDirect3DIndexBuffer9** ppIndexBuffer,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(CreateRenderTarget)(THIS_ UINT Width,UINT Height,D3DFORMAT Format,D3DMULTISAMPLE_TYPE MultiSample,DWORD MultisampleQuality,BOOL Lockable,IDirect3DSurface9** ppSurface,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(CreateDepthStencilSurface)(THIS_ UINT Width,UINT Height,D3DFORMAT Format,D3DMULTISAMPLE_TYPE MultiSample,DWORD MultisampleQuality,BOOL Discard,IDirect3DSurface9** ppSurface,HANDLE* pSharedHandle) PURE;
	#STDMETHOD(UpdateSurface)(THIS_ IDirect3DSurface9* pSourceSurface,CONST RECT* pSourceRect,IDirect3DSurface9* pDestinationSurface,CONST POINT* pDestPoint) PURE;
	#STDMETHOD(UpdateTexture)(THIS_ IDirect3DBaseTexture9* pSourceTexture,IDirect3DBaseTexture9* pDestinationTexture) PURE;
	#STDMETHOD(GetRenderTargetData)(THIS_ IDirect3DSurface9* pRenderTarget,IDirect3DSurface9* pDestSurface) PURE;
	#STDMETHOD(GetFrontBufferData)(THIS_ UINT iSwapChain,IDirect3DSurface9* pDestSurface) PURE;
	#STDMETHOD(StretchRect)(THIS_ IDirect3DSurface9* pSourceSurface,CONST RECT* pSourceRect,IDirect3DSurface9* pDestSurface,CONST RECT* pDestRect,D3DTEXTUREFILTERTYPE Filter) PURE;
	#STDMETHOD(ColorFill)(THIS_ IDirect3DSurface9* pSurface,CONST RECT* pRect,D3DCOLOR color) PURE;
#STDMETHOD(CreateOffscreenPlainSurface)(THIS_ UINT Width,UINT Height,D3DFORMAT Format,D3DPOOL Pool,IDirect3DSurface9** ppSurface,HANDLE* pSharedHandle) PURE;
#STDMETHOD(SetRenderTarget)(THIS_ DWORD RenderTargetIndex,IDirect3DSurface9* pRenderTarget) PURE;
#STDMETHOD(GetRenderTarget)(THIS_ DWORD RenderTargetIndex,IDirect3DSurface9** ppRenderTarget) PURE;
#STDMETHOD(SetDepthStencilSurface)(THIS_ IDirect3DSurface9* pNewZStencil) PURE;
#STDMETHOD(GetDepthStencilSurface)(THIS_ IDirect3DSurface9** ppZStencilSurface) PURE;
#STDMETHOD(BeginScene)(THIS) PURE;
#STDMETHOD(EndScene)(THIS) PURE;
#STDMETHOD(Clear)(THIS_ DWORD Count,CONST D3DRECT* pRects,DWORD Flags,D3DCOLOR Color,float Z,DWORD Stencil) PURE;
#STDMETHOD(SetTransform)(THIS_ D3DTRANSFORMSTATETYPE State,CONST D3DMATRIX* pMatrix) PURE;
#STDMETHOD(GetTransform)(THIS_ D3DTRANSFORMSTATETYPE State,D3DMATRIX* pMatrix) PURE;
#STDMETHOD(MultiplyTransform)(THIS_ D3DTRANSFORMSTATETYPE,CONST D3DMATRIX*) PURE;
#STDMETHOD(SetViewport)(THIS_ CONST D3DVIEWPORT9* pViewport) PURE;
#STDMETHOD(GetViewport)(THIS_ D3DVIEWPORT9* pViewport) PURE;
#STDMETHOD(SetMaterial)(THIS_ CONST D3DMATERIAL9* pMaterial) PURE;
#STDMETHOD(GetMaterial)(THIS_ D3DMATERIAL9* pMaterial) PURE;
#STDMETHOD(SetLight)(THIS_ DWORD Index,CONST D3DLIGHT9*) PURE;
#STDMETHOD(GetLight)(THIS_ DWORD Index,D3DLIGHT9*) PURE;
#STDMETHOD(LightEnable)(THIS_ DWORD Index,BOOL Enable) PURE;
#STDMETHOD(GetLightEnable)(THIS_ DWORD Index,BOOL* pEnable) PURE;
#STDMETHOD(SetClipPlane)(THIS_ DWORD Index,CONST float* pPlane) PURE;
#STDMETHOD(GetClipPlane)(THIS_ DWORD Index,float* pPlane) PURE;
#STDMETHOD(SetRenderState)(THIS_ D3DRENDERSTATETYPE State,DWORD Value) PURE;
#STDMETHOD(GetRenderState)(THIS_ D3DRENDERSTATETYPE State,DWORD* pValue) PURE;
#STDMETHOD(CreateStateBlock)(THIS_ D3DSTATEBLOCKTYPE Type,IDirect3DStateBlock9** ppSB) PURE;
#STDMETHOD(BeginStateBlock)(THIS) PURE;
#STDMETHOD(EndStateBlock)(THIS_ IDirect3DStateBlock9** ppSB) PURE;
#STDMETHOD(SetClipStatus)(THIS_ CONST D3DCLIPSTATUS9* pClipStatus) PURE;
#STDMETHOD(GetClipStatus)(THIS_ D3DCLIPSTATUS9* pClipStatus) PURE;
#STDMETHOD(GetTexture)(THIS_ DWORD Stage,IDirect3DBaseTexture9** ppTexture) PURE;
#STDMETHOD(SetTexture)(THIS_ DWORD Stage,IDirect3DBaseTexture9* pTexture) PURE;
#STDMETHOD(GetTextureStageState)(THIS_ DWORD Stage,D3DTEXTURESTAGESTATETYPE Type,DWORD* pValue) PURE;
#STDMETHOD(SetTextureStageState)(THIS_ DWORD Stage,D3DTEXTURESTAGESTATETYPE Type,DWORD Value) PURE;
#STDMETHOD(GetSamplerState)(THIS_ DWORD Sampler,D3DSAMPLERSTATETYPE Type,DWORD* pValue) PURE;
#STDMETHOD(SetSamplerState)(THIS_ DWORD Sampler,D3DSAMPLERSTATETYPE Type,DWORD Value) PURE;
#STDMETHOD(ValidateDevice)(THIS_ DWORD* pNumPasses) PURE;
#STDMETHOD(SetPaletteEntries)(THIS_ UINT PaletteNumber,CONST PALETTEENTRY* pEntries) PURE;
#STDMETHOD(GetPaletteEntries)(THIS_ UINT PaletteNumber,PALETTEENTRY* pEntries) PURE;
#STDMETHOD(SetCurrentTexturePalette)(THIS_ UINT PaletteNumber) PURE;
#STDMETHOD(GetCurrentTexturePalette)(THIS_ UINT *PaletteNumber) PURE;
#STDMETHOD(SetScissorRect)(THIS_ CONST RECT* pRect) PURE;
#STDMETHOD(GetScissorRect)(THIS_ RECT* pRect) PURE;
#STDMETHOD(SetSoftwareVertexProcessing)(THIS_ BOOL bSoftware) PURE;
#STDMETHOD_(BOOL, GetSoftwareVertexProcessing)(THIS) PURE;
#STDMETHOD(SetNPatchMode)(THIS_ float nSegments) PURE;
#STDMETHOD_(float, GetNPatchMode)(THIS) PURE;
#STDMETHOD(DrawPrimitive)(THIS_ D3DPRIMITIVETYPE PrimitiveType,UINT StartVertex,UINT PrimitiveCount) PURE;
#STDMETHOD(DrawIndexedPrimitive)(THIS_ D3DPRIMITIVETYPE,INT BaseVertexIndex,UINT MinVertexIndex,UINT NumVertices,UINT startIndex,UINT primCount) PURE;
#STDMETHOD(DrawPrimitiveUP)(THIS_ D3DPRIMITIVETYPE PrimitiveType,UINT PrimitiveCount,CONST void* pVertexStreamZeroData,UINT VertexStreamZeroStride) PURE;
#STDMETHOD(DrawIndexedPrimitiveUP)(THIS_ D3DPRIMITIVETYPE PrimitiveType,UINT MinVertexIndex,UINT NumVertices,UINT PrimitiveCount,CONST void* pIndexData,D3DFORMAT IndexDataFormat,CONST void* pVertexStreamZeroData,UINT VertexStreamZeroStride) PURE;
#STDMETHOD(ProcessVertices)(THIS_ UINT SrcStartIndex,UINT DestIndex,UINT VertexCount,IDirect3DVertexBuffer9* pDestBuffer,IDirect3DVertexDeclaration9* pVertexDecl,DWORD Flags) PURE;
#STDMETHOD(CreateVertexDeclaration)(THIS_ CONST D3DVERTEXELEMENT9* pVertexElements,IDirect3DVertexDeclaration9** ppDecl) PURE;
#STDMETHOD(SetVertexDeclaration)(THIS_ IDirect3DVertexDeclaration9* pDecl) PURE;
#STDMETHOD(GetVertexDeclaration)(THIS_ IDirect3DVertexDeclaration9** ppDecl) PURE;
#STDMETHOD(SetFVF)(THIS_ DWORD FVF) PURE;
#STDMETHOD(GetFVF)(THIS_ DWORD* pFVF) PURE;
#STDMETHOD(CreateVertexShader)(THIS_ CONST DWORD* pFunction,IDirect3DVertexShader9** ppShader) PURE;
#STDMETHOD(SetVertexShader)(THIS_ IDirect3DVertexShader9* pShader) PURE;
#STDMETHOD(GetVertexShader)(THIS_ IDirect3DVertexShader9** ppShader) PURE;
#STDMETHOD(SetVertexShaderConstantF)(THIS_ UINT StartRegister,CONST float* pConstantData,UINT Vector4fCount) PURE;
#STDMETHOD(GetVertexShaderConstantF)(THIS_ UINT StartRegister,float* pConstantData,UINT Vector4fCount) PURE;
#STDMETHOD(SetVertexShaderConstantI)(THIS_ UINT StartRegister,CONST int* pConstantData,UINT Vector4iCount) PURE;
#STDMETHOD(GetVertexShaderConstantI)(THIS_ UINT StartRegister,int* pConstantData,UINT Vector4iCount) PURE;
#STDMETHOD(SetVertexShaderConstantB)(THIS_ UINT StartRegister,CONST BOOL* pConstantData,UINT  BoolCount) PURE;
#STDMETHOD(GetVertexShaderConstantB)(THIS_ UINT StartRegister,BOOL* pConstantData,UINT BoolCount) PURE;
#STDMETHOD(SetStreamSource)(THIS_ UINT StreamNumber,IDirect3DVertexBuffer9* pStreamData,UINT OffsetInBytes,UINT Stride) PURE;
#STDMETHOD(GetStreamSource)(THIS_ UINT StreamNumber,IDirect3DVertexBuffer9** ppStreamData,UINT* OffsetInBytes,UINT* pStride) PURE;
#STDMETHOD(SetStreamSourceFreq)(THIS_ UINT StreamNumber,UINT Divider) PURE;
#STDMETHOD(GetStreamSourceFreq)(THIS_ UINT StreamNumber,UINT* Divider) PURE;
#STDMETHOD(SetIndices)(THIS_ IDirect3DIndexBuffer9* pIndexData) PURE;
#STDMETHOD(GetIndices)(THIS_ IDirect3DIndexBuffer9** ppIndexData) PURE;
#STDMETHOD(CreatePixelShader)(THIS_ CONST DWORD* pFunction,IDirect3DPixelShader9** ppShader) PURE;
#STDMETHOD(SetPixelShader)(THIS_ IDirect3DPixelShader9* pShader) PURE;
#STDMETHOD(GetPixelShader)(THIS_ IDirect3DPixelShader9** ppShader) PURE;
#STDMETHOD(SetPixelShaderConstantF)(THIS_ UINT StartRegister,CONST float* pConstantData,UINT Vector4fCount) PURE;
#STDMETHOD(GetPixelShaderConstantF)(THIS_ UINT StartRegister,float* pConstantData,UINT Vector4fCount) PURE;
#STDMETHOD(SetPixelShaderConstantI)(THIS_ UINT StartRegister,CONST int* pConstantData,UINT Vector4iCount) PURE;
#STDMETHOD(GetPixelShaderConstantI)(THIS_ UINT StartRegister,int* pConstantData,UINT Vector4iCount) PURE;
#STDMETHOD(SetPixelShaderConstantB)(THIS_ UINT StartRegister,CONST BOOL* pConstantData,UINT  BoolCount) PURE;
#STDMETHOD(GetPixelShaderConstantB)(THIS_ UINT StartRegister,BOOL* pConstantData,UINT BoolCount) PURE;
#STDMETHOD(DrawRectPatch)(THIS_ UINT Handle,CONST float* pNumSegs,CONST D3DRECTPATCH_INFO* pRectPatchInfo) PURE;
#STDMETHOD(DrawTriPatch)(THIS_ UINT Handle,CONST float* pNumSegs,CONST D3DTRIPATCH_INFO* pTriPatchInfo) PURE;
#STDMETHOD(DeletePatch)(THIS_ UINT Handle) PURE;
#STDMETHOD(CreateQuery)(THIS_ D3DQUERYTYPE Type,IDirect3DQuery9** ppQuery) PURE;
    
    
########################################
# IDirect3D9
# https://docs.microsoft.com/en-us/windows/win32/api/d3d9/nn-d3d9-idirect3d9
########################################
	
IDirect3D9._methods_ = [
	#STDMETHOD(RegisterSoftwareDevice)(THIS_ void* pInitializeFunction) PURE;
	COMMETHOD([], HRESULT, 'RegisterSoftwareDevice',
			(['in'], c_void_p, 'pInitializeFunction')),
	
	#STDMETHOD_(UINT, GetAdapterCount)(THIS) PURE;
	COMMETHOD([], UINT, 'GetAdapterCount',
			),
			
	#STDMETHOD(GetAdapterIdentifier)(THIS_ UINT Adapter,DWORD Flags,D3DADAPTER_IDENTIFIER9* pIdentifier) PURE;
	COMMETHOD([], HRESULT, 'GetAdapterIdentifier',
			(['in'], UINT, 'Adapter'),
			(['in'], DWORD, 'Flags'),
			(['out'], POINTER(D3DADAPTER_IDENTIFIER9), 'pIdentifier')),
			
	#STDMETHOD_(UINT, GetAdapterModeCount)(THIS_ UINT Adapter,D3DFORMAT Format) PURE;
	COMMETHOD([], UINT, 'GetAdapterModeCount',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DFORMAT, 'Format')),

	#STDMETHOD(EnumAdapterModes)(THIS_ UINT Adapter,D3DFORMAT Format,UINT Mode,D3DDISPLAYMODE* pMode) PURE;
	COMMETHOD([], HRESULT, 'EnumAdapterModes',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DFORMAT, 'Format'),
			(['in'], UINT, 'Mode'),
			(['out'], POINTER(D3DDISPLAYMODE), 'pMode')),
			
	#STDMETHOD(GetAdapterDisplayMode)(THIS_ UINT Adapter,D3DDISPLAYMODE* pMode) PURE;
	COMMETHOD([], HRESULT, 'GetAdapterDisplayMode',
			(['in'], UINT, 'Adapter'),
			(['out'], POINTER(D3DDISPLAYMODE), 'pMode')),
			
	#STDMETHOD(CheckDeviceType)(THIS_ UINT iAdapter,D3DDEVTYPE DevType,D3DFORMAT DisplayFormat,D3DFORMAT BackBufferFormat,BOOL bWindowed) PURE;
	COMMETHOD([], HRESULT, 'CheckDeviceType',
			(['in'], UINT, 'iAdapter'),
			(['in'], D3DDEVTYPE, 'DevType'),
			(['in'], D3DFORMAT, 'DisplayFormat'),
			(['in'], D3DFORMAT, 'BackBufferFormat'),
			(['in'], BOOL, 'bWindowed')),
			
	#STDMETHOD(CheckDeviceFormat)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT AdapterFormat,DWORD Usage,D3DRESOURCETYPE RType,D3DFORMAT CheckFormat) PURE;
	COMMETHOD([], HRESULT, 'CheckDeviceFormat',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DDEVTYPE, 'DeviceType'),
			(['in'], D3DFORMAT, 'AdapterFormat'),
			(['in'], DWORD, 'Usage'),
			(['in'], D3DRESOURCETYPE, 'RType'),
			(['in'], D3DFORMAT, 'CheckFormat')),
			
	#STDMETHOD(CheckDeviceMultiSampleType)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT SurfaceFormat,BOOL Windowed,D3DMULTISAMPLE_TYPE MultiSampleType,DWORD* pQualityLevels) PURE;
	COMMETHOD([], HRESULT, 'CheckDeviceMultiSampleType',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DDEVTYPE, 'DeviceType'),
			(['in'], D3DFORMAT, 'SourceFormat'),
			(['in'], BOOL, 'Windowed'),
			(['in'], D3DMULTISAMPLE_TYPE, 'MultiSampleType'),
			(['in'], POINTER(DWORD), 'pQualityLevels')),
			
	#STDMETHOD(CheckDepthStencilMatch)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT AdapterFormat,D3DFORMAT RenderTargetFormat,D3DFORMAT DepthStencilFormat) PURE;
	COMMETHOD([], HRESULT, 'CheckDepthStencilMatch',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DDEVTYPE, 'DeviceType'),
			(['in'], D3DFORMAT, 'AdapterFormat'),
			(['in'], D3DFORMAT, 'RenderTargetFormat'),
			(['in'], D3DFORMAT, 'DepthStencilFormat')),
			
	#STDMETHOD(CheckDeviceFormatConversion)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT SourceFormat,D3DFORMAT TargetFormat) PURE;
	COMMETHOD([], HRESULT, 'CheckDeviceFormatConversion',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DDEVTYPE, 'DeviceType'),
			(['in'], D3DFORMAT, 'SourceFormat'),
			(['in'], D3DFORMAT, 'TargetFormat')),
			
	#STDMETHOD(GetDeviceCaps)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DCAPS9* pCaps) PURE;
	COMMETHOD([], HRESULT, 'GetDeviceCaps',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DDEVTYPE, 'DeviceType'),
			(['out'], POINTER(D3DCAPS9), 'pCaps')),
			
	#STDMETHOD_(HMONITOR, GetAdapterMonitor)(THIS_ UINT Adapter) PURE;
	COMMETHOD([], HMONITOR, 'GetAdapterMonitor',
			(['in'], UINT, 'Adapter')),
			
	#STDMETHOD(CreateDevice)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,HWND hFocusWindow,DWORD BehaviorFlags,D3DPRESENT_PARAMETERS* pPresentationParameters,IDirect3DDevice9** ppReturnedDeviceInterface) PURE;
	COMMETHOD([], HRESULT, 'CreateDevice',
			(['in'], UINT, 'Adapter'),
			(['in'], D3DDEVTYPE, 'DeviceType'),
			(['in'], HWND, 'hFocusWindow'),
			(['in'], DWORD, 'BehaviorFlags'),
			(['in'], POINTER(D3DPRESENT_PARAMETERS), 'pPresentationParameters'),
			(['out'], POINTER(POINTER(IDirect3DDevice9)), 'ppReturnedDeviceInterface'))
		]
	

#DECLARE_INTERFACE_(IDirect3D9, IUnknown)
#{
#    /*** IUnknown methods ***/
#    STDMETHOD(QueryInterface)(THIS_ REFIID riid, void** ppvObj) PURE;
#    STDMETHOD_(ULONG,AddRef)(THIS) PURE;
#    STDMETHOD_(ULONG,Release)(THIS) PURE;
#
#    /*** IDirect3D9 methods ***/
#    STDMETHOD(RegisterSoftwareDevice)(THIS_ void* pInitializeFunction) PURE;
#    STDMETHOD_(UINT, GetAdapterCount)(THIS) PURE;
#    STDMETHOD(GetAdapterIdentifier)(THIS_ UINT Adapter,DWORD Flags,D3DADAPTER_IDENTIFIER9* pIdentifier) PURE;
#    STDMETHOD_(UINT, GetAdapterModeCount)(THIS_ UINT Adapter,D3DFORMAT Format) PURE;
#    STDMETHOD(EnumAdapterModes)(THIS_ UINT Adapter,D3DFORMAT Format,UINT Mode,D3DDISPLAYMODE* pMode) PURE;
#    STDMETHOD(GetAdapterDisplayMode)(THIS_ UINT Adapter,D3DDISPLAYMODE* pMode) PURE;
#    STDMETHOD(CheckDeviceType)(THIS_ UINT iAdapter,D3DDEVTYPE DevType,D3DFORMAT DisplayFormat,D3DFORMAT BackBufferFormat,BOOL bWindowed) PURE;
#    STDMETHOD(CheckDeviceFormat)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT AdapterFormat,DWORD Usage,D3DRESOURCETYPE RType,D3DFORMAT CheckFormat) PURE;
#    STDMETHOD(CheckDeviceMultiSampleType)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT SurfaceFormat,BOOL Windowed,D3DMULTISAMPLE_TYPE MultiSampleType,DWORD* pQualityLevels) PURE;
#    STDMETHOD(CheckDepthStencilMatch)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT AdapterFormat,D3DFORMAT RenderTargetFormat,D3DFORMAT DepthStencilFormat) PURE;
#    STDMETHOD(CheckDeviceFormatConversion)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DFORMAT SourceFormat,D3DFORMAT TargetFormat) PURE;
#    STDMETHOD(GetDeviceCaps)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,D3DCAPS9* pCaps) PURE;
#    STDMETHOD_(HMONITOR, GetAdapterMonitor)(THIS_ UINT Adapter) PURE;
#    STDMETHOD(CreateDevice)(THIS_ UINT Adapter,D3DDEVTYPE DeviceType,HWND hFocusWindow,DWORD BehaviorFlags,D3DPRESENT_PARAMETERS* pPresentationParameters,IDirect3DDevice9** ppReturnedDeviceInterface) PURE;
#
#    /*** Helper information ***/
#    LPCWSTR Version;
#}
