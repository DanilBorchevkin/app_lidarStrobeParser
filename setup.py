import sys, os
from cx_Freeze import setup, Executable

os.environ['TCL_LIBRARY'] = r'C:\Anaconda3\tcl\tcl8.6'
os.environ['TK_LIBRARY'] = r'C:\Anaconda3\tcl\tcl8.6'

setup(
    name = "Lidar Strobe Parses",
    version = "0.1",
    description = "",
    executables = [Executable("lidarStrobeParser.py", base = "Win32GUI")])