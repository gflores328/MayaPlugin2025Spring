import sys
prjPath = "D:/profile redirect/gaflore5/MayaPlugin2025Spring/src"
moduleDir = "D:/profile redirect/gaflore5"

#prjPath = "C:/Users/Gabe/Documents/GitHub/Test/MayaPlugin2025Spring/src"

if prjPath not in sys.path:
    sys.path.append(prjPath)

if moduleDir not in sys.path:
    sys.path.append(moduleDir)

