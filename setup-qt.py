from cx_Freeze import setup, Executable
import os


executables = [
    Executable('NEWS-qt.py',
               base='Win32GUI',
               icon='news.ico'
               )
]

includes = []
include_files = []
                 
options = {
    'build_exe': {
        'optimize': 2,
        "includes": includes,
        "include_files": include_files
    }
}


setup(
      name='News',
      version='0.0.3',
      description='Новости',
      author = "Крезуб П.Н.",
      options = options,
      executables=executables
      )