# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('config.py', '.'), ('Info.plist', '.')],
    hiddenimports=[
        'google.generativeai',
        'tkinter'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],  # Không bao gồm binaries và zipfiles trong exe
    exclude_binaries=True,  # Quan trọng cho macOS
    name='XML Translator',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    target_arch='universal2',  # Hỗ trợ cả Intel và Apple Silicon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='XML Translator'
)

app = BUNDLE(
    coll,  # Sử dụng COLLECT thay vì EXE
    name='XML Translator.app',
    icon=None,
    bundle_identifier='com.xmltranslator.app',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'CFBundleVersion': '1.0.0',
        'NSHighResolutionCapable': True,
        'CFBundleDisplayName': 'XML Translator',
        'CFBundlePackageType': 'APPL',
    },
) 