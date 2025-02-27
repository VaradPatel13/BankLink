# BankLink.spec
# This spec file packages the BankLink app into a single executable.

import sys
import os
from kivy_deps import sdl2, glew
from PyInstaller.utils.hooks import collect_data_files

# Define the assets you want to include.
# Adjust the folder paths as needed if your assets are in different locations.
datas = [
    # Include the entire Fonts folder (source folder, target folder)
    ("Pages/assets/Fonts", "Pages/assets/Fonts"),
    # Include Images if applicable:
    ("Pages/assets/Images", "Pages/assets/Images"),
    # Include any config files like Firebase config
    ("firebase_config.json", "."),
]

# Hidden imports ensure that PyInstaller packages modules that are imported dynamically.
hiddenimports = [
    "firebase_admin",
    "kivymd",
    "bcrypt",
    "pyrebase4",
    "qrcode",
    # Add additional modules if your project uses them.
]

# Analysis collects information about your scripts and dependencies.
a = Analysis(
    ['main.py'],          # Your entry point script
    pathex=[os.path.abspath(".")],  # The search path for imports (current folder)
    binaries=[],          # Additional binaries (if needed)
    datas=datas + collect_data_files("kivymd"),  # Add asset folders and any data files from kivymd
    hiddenimports=hiddenimports,
    hookspath=[],         # You can add custom hook directories here
    runtime_hooks=[],     # Runtime hooks if necessary
    excludes=[],          # Exclude any unnecessary modules
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=None,
    noarchive=False,
)

# Include Kivy dependency binaries (for example, SDL2 and GLEW DLLs).
a.binaries += sdl2.dep_bins + glew.dep_bins

# Package all pure Python modules into a PYZ archive.
pyz = PYZ(a.pure, a.zipped_data, cipher=None)

# Create the final executable.
exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name="BankLink",       # Name of your application
    debug=False,           # Set to True to enable debugging
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,              # Compress the executable with UPX (if installed)
    console=False,         # Set to True if you need a console window for debugging
)

# If you want a one-folder build instead of a single file, you can remove the --onefile option.
