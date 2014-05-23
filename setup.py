import sys
from cx_Freeze import setup, Executable

build_exe_options = {"packages": ["sys", "matplotlib"],
                     "include_files": ["static", "license.txt", "gnu-gpl.txt"],
                     "icon": "static/logo-small.gif"
}

base = None
if sys.platform == "win32":
    bas = "Win32GUI"

setup(  name = "SeatingChartCreator",
        version = "0.1",
        description = "An application for creating an optimal seating chart",
        options = {"build_exe": build_exe_options},
        data_files = [('static', ['static/logo-small.gif',
'static/people-example.gif',
'static/tables-example.gif'])],
        executables = [Executable("SeatingChartCreator.py", base=base)])
