from cx_Freeze import setup, Executable
import os


executables = [
    Executable('NEWS.py',
               base='Win32GUI',
               icon='news.ico'
               )
]

includes = []
include_files = [r"D:\Program Files\Python_365\DLLs\tcl86t.dll",
                 r"D:\Program Files\Python_365\DLLs\tk86t.dll"]
                 
options = {
    'build_exe': {
        'optimize': 2,
        "includes": includes,
        "include_files": include_files
    }
}

os.environ['TCL_LIBRARY'] = r'D:\Program Files\Python_365\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'D:\Program Files\Python_365\tcl\tk8.6'

setup(
      name='News',
      version='0.0.2',
      description='Новости',
      author = "Крезуб П.Н.",
      options = options,
      executables=executables
      )