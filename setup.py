import sys
from cx_Freeze import setup, Executable

base = None

if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'include_files': ['myapp'],  # Add any additional files or data needed here
    },
}

executables = [
    Executable('probitan.py', base=base, icon='myapp/appfiles/images/bg/icon.ico', target_name='Probitan.exe'),  # Replace 'your_main_script.py' with your main script
]

setup(
    name='Probitan',
    version='1.0',
    description='PROBITAN - An Equipment Process Reliability Analytical Tool.',
    options=options,
    executables=executables
)
