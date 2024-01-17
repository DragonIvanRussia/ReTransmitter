from cx_Freeze import setup, Executable

includes = ['sounds', 'images', 'fonts']

setup(
    name="ReTransmitter",
    version="0.1",
    description="My GUI application!",
    options={"build_exe": {'includes':includes, "packages":["pygame", 'foundation.py', 'menu.py']}},
    executables=[Executable("main.py")],
)
