import sys
from cx_Freeze import setup, Executable

includes = ['sounds', 'images', 'fonts']

setup(
    name="ReTransmitter",
    version="0.1",
    description="A simple Python Rhythm game",
    options={"build_exe": {'includes':includes, "packages":["pygame", 'foundation.py', 'menu.py']}},
    executables=[Executable("main.py")],
)
