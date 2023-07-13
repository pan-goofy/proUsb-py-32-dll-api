from cx_Freeze import setup, Executable
path_platforms = ( "E:\card-py32\d12.dll", "E:\card-py32\d12c.dll","E:\card-py32\proRFL.dll","E:\card-py32\config.ini" )#pyqt5大包围windows软件的dll文件
includefiles = [path_platforms]

build_exe_options = {"packages": ["os"],
                     "excludes": ["tkinter"],
                     "include_files": includefiles,}
setup(
    name="cardPro",
    version="1.0",
    description="pornHub发卡器接口",
    executables=[Executable("main.py", base="Win32GUI")]

)