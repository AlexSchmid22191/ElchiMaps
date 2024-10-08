# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['ElchiMaps.py'],
    pathex=[],
    binaries=[],
    datas=[('Interface/Icons', 'Interface/Icons'),
           ('Interface/Fonts', 'Interface/Fonts'),
           ('Interface/Styles', 'Interface/Styles'),
           ('License', 'License'),
           ('.venv/Lib/site-packages/xrayutilities/xrayutilities_default.conf', 'xrayutilities'),
           ('.venv/Lib/site-packages/xrayutilities/VERSION', 'xrayutilities'),],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ElchiMaps',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Interface/Icons/Logo.ico',
    contents_directory='.'
)

exe2 = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='ElchiMapsDebug',
    debug=True,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Interface/Icons/Logo.ico',
    contents_directory='.'
)


coll = COLLECT(
    exe,
    exe2,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='ElchiMaps',
)
