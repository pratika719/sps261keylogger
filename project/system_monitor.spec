# -*- mode: python ; coding: utf-8 -*-
"""
PyInstaller specification file for System Monitor
Generates a standalone Windows executable with all dependencies

Usage:
    pyinstaller system_monitor.spec

This will create:
    - dist/SystemMonitor.exe (standalone executable)
    - All dependencies bundled inside
"""

block_cipher = None

a = Analysis(
    ['system_monitor.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('config.example.ini', '.'),  # Include example config
    ],
    hiddenimports=[
        'win32clipboard',
        'win32api',
        'win32con',
        'pywintypes',
        'sounddevice',
        'scipy.io.wavfile',
        'cryptography.fernet',
        'PIL.ImageGrab',
        'pynput.keyboard',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='SystemMonitor',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,  # Set to False to hide console window
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon=None,  # Add path to .ico file if you have one
    version='version_info.txt',  # Optional: version information
)

# Optional: Create a COLLECT for one-folder distribution
# Uncomment below if you prefer one-folder instead of one-file

# coll = COLLECT(
#     exe,
#     a.binaries,
#     a.zipfiles,
#     a.datas,
#     strip=False,
#     upx=True,
#     upx_exclude=[],
#     name='SystemMonitor',
# )
