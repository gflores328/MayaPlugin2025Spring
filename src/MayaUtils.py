from PySide2.QtWidgets import QMainWindow, QWidget #imports classes from PySide2.QtWidgets
from PySide2.QtCore import Qt #imports the Qt class from PySide2.QtCore
import maya.OpenMayaUI as omui #imports access to the Maya UI and names it as omui
import shiboken2 #imports shiboken2
import maya.cmds as mc

def IsMesh(obj):
    shapes = mc.listRelatives(obj, s = True)
    if not shapes:
        return False
    
    for s in shapes:
        if mc.objectType(s) == "mesh":
            return True
        
    return False

def IsSkin(obj):
    return mc.objectType(obj) == "skinCluster"

def IsJoint(obj):
    return mc.objectType(obj) == "joint"

def GetUpperStream(obj):
    return mc.listConnections(obj, s = True, d = False, sh = True)

def GetLowerStream(obj):
    return mc.listConnections(obj, s = False, d = True, sh = True)

def GetAllConnectionsIn(obj, nextFunc, filter = None):
    allFound = []
    nexts = nextFunc(obj)
    searchDepth = 100
    while nexts and searchDepth > 0:
        searchDepth -= 1
        for next in nexts:
            allFound.append(next)

        nexts = nextFunc(nexts)
        if nexts:
            nexts = [x for x in nexts if x not in allFound]

    if not filter:
        return list (allFound)
    
    filtered = []
    for found in allFound:
        if filter(found):
            filtered.append(found)

    return filtered

def GetMayaMainWindow()->QMainWindow: #Definition of a function called GetMayaMainWindow that must return a QMainWindow
    mainWindow = omui.MQtUtil.mainWindow() #mainWindow is set to the main window of Maya gotten throught the omui import
    return shiboken2.wrapInstance(int(mainWindow), QMainWindow) #creates a wrapper for mainWindow using its memory adress and wraps as a QMainWindow class

def DeleteWidgetWithName(name): #Definition of a function calledDeleteWidgetWithName that takes a string as a parameter
    for widget in GetMayaMainWindow().findChildren(QWidget, name): #Loops thorugh each window that is open in Maya that has the name passed through the function
        widget.deleteLater() #Deletes the reference of the widget from memory

class MayaWindow(QWidget): #Definition for a class called MayaWindow that inherits from the QWidgetClass
    def __init__(self): #Definition for the classses constructor
        super().__init__(parent = GetMayaMainWindow()) #Calls the constructor of the parent class and sets that widgets parent as the return of GetMayaMainWindow
        DeleteWidgetWithName(self.GetWidgetUniqueName()) #Calls DeleteWidgetWithName and passes the return of the GetWidgetWithUniqueName function as the name of the widget to be deleted
        self.setWindowFlags(Qt.WindowType.Window) #Sets the window flags of the classes widget to be of WindowType Window
        self.setObjectName(self.GetWidgetUniqueName()) #Sets the name of the classes widget inherited to be the return of GetWidgetUniqueName

    def GetWidgetUniqueName(self): #Definition for a function called GetWidgetWithUniqueName that has no parameters
        return "fdfdfdfdfdfdff8732t5c8475tb38745btc982sdfsdf7345tcb473" #returns a string