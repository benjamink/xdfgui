"""
py2app setup script for creating macOS application bundle.
"""
from setuptools import setup

APP = ['xdfgui/cli.py']
DATA_FILES = []
OPTIONS = {
    'argv_emulation': False,
    'packages': ['tkinter', 'xdfgui', 'amitools', 'lhafile'],
    'excludes': ['pytest', 'test'],
    'iconfile': None,  # Add an .icns file path here if you have one
    'plist': {
        'CFBundleName': 'xdfgui',
        'CFBundleDisplayName': 'xdfgui',
        'CFBundleIdentifier': 'com.xdfgui.app',
        'CFBundleVersion': '0.1.0',
        'CFBundleShortVersionString': '0.1.0',
        'NSHighResolutionCapable': True,
    }
}

setup(
    name='xdfgui',
    version='0.1.0',
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
)
