# -*- mode: python ; coding: utf-8 -*-

a = Analysis(
    ['xdfgui/cli.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=['xdfgui', 'xdfgui.gui', 'xdfgui.xdftool_wrapper', 'xdfgui.lha_split', 'amitools', 'lhafile'],
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
    name='xdfgui',
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
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='xdfgui',
)
app = BUNDLE(
    coll,
    name='xdfgui.app',
    icon=None,
    bundle_identifier='com.xdfgui.app',
    info_plist={
        'NSHighResolutionCapable': True,
        'CFBundleName': 'xdfgui',
        'CFBundleDisplayName': 'xdfgui',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
    },
)
