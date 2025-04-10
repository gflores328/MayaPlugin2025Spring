from PySide2.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QMainWindow, QMessageBox, QPushButton, QSlider, QVBoxLayout, QWidget #imports classes from PySide2.QtWidgets
from PySide2.QtCore import Qt #imports the Qt class from PySide2.QtCore
from maya.OpenMaya import MVector
import maya.OpenMayaUI as omui #imports access to the Maya UI and names it as omui
import maya.mel as mel
import shiboken2 #imports shiboken2

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
 
import maya.cmds as mc #imports maya.cmds and names it as mc
class LimbRigger: #Definition for a class called LimbRigger
    def __init__(self): #Definition for the constructor of the LimbRigger class
        self.root = "" #sets the classes root variable to be an empty string
        self.mid = "" #sets the classes mid variable to be an empty string
        self.end = "" #sets the classes end variable to be an empty string
        self.controllerSize = 5 #sets the class controllerSize int variable to 5
        self.colorIndex = 0 # ADDED FOR 4/10 ASSIGNMENT

    def FindJointsBasedOnSelection(self): #Definition for a function called FindJointsBasedOnSelection
        try: #The start of a a try block
            self.root = mc.ls(sl = True, type = "joint")[0] #Sets self.root to be the name of what is selected in Maya if it is a joint. Gets the first selected object 
            self.mid = mc.listRelatives(self.root, c = True, type = "joint")[0] #Sets self.mid to be the first child of self.root if it is a joint
            self.end = mc.listRelatives(self.mid, c = True, type = "joint")[0] #Sets self.end to be the first child of self.mid if it is a joint
        except Exception as e: # The start of an except block
            raise Exception("Wrong Selection, please select the first joint of the limb!") #Raises an exception if anything in the try block failed

    def CreateFKControllerForJoint(self, jntName): #Definition for a function called CreateFKControllerForJoint  that takes a string as a parameter as jntName
        ctrlName = "ac_l_fk_" + jntName #sets the ctrlName variable to be "ac_l_fk" plus jntName
        ctrlGrpName = ctrlName + "_grp" #sets the ctrlGrpName variable to be ctrlName + "_grp"
        mc.circle(name = ctrlName, radius = self.controllerSize, normal = (1,0,0)) #creates a circle and names it the value of ctrlname and sets its size to controllerSize
        mc.group(ctrlName, n = ctrlGrpName) #puts the circle into a group and names the group as ctrlGrpName
        mc.matchTransform(ctrlGrpName, jntName) #Matches the transformation of the circle group to the location of the jntName joint
        mc.orientConstraint(ctrlName, jntName) #Orient contraints jntName joint to ctrlName circle
        return ctrlName, ctrlGrpName #returns ctrlName and ctrlGrpName
    
    def CreateBoxController(self, name):
        mel.eval(f"curve -n {name} -d 1 -p 0.5 0.5 0.5 -p 0.5 0.5 -0.5 -p 0.5 -0.5 -0.5 -p 0.5 -0.5 0.5 -p 0.5 0.5 0.5 -p -0.5 0.5 0.5 -p -0.5 -0.5 0.5 -p 0.5 -0.5 0.5 -p -0.5 -0.5 0.5 -p -0.5 -0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 0.5 0.5 -p -0.5 0.5 -0.5 -p 0.5 0.5 -0.5 -p -0.5 0.5 -0.5 -p -0.5 -0.5 -0.5 -p 0.5 -0.5 -0.5 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 -k 13 -k 14 -k 15 -k 16 ;")
        mc.scale(self.controllerSize, self.controllerSize, self.controllerSize, name)
        mc.makeIdentity(name, apply = True)
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
    
    def CreatePlusController(self, name):
        mel.eval(f"curve -n {name} -d 1 -p 7 1 0 -p 5 1 0 -p 5 -1 0 -p 3 -1 0 -p 3 -3 0 -p 5 -3 0 -p 5 -5 0 -p 7 -5 0 -p 7 -3 0 -p 9 -3 0 -p 9 -1 0 -p 7 -1 0 -p 7 1 0 -k 0 -k 1 -k 2 -k 3 -k 4 -k 5 -k 6 -k 7 -k 8 -k 9 -k 10 -k 11 -k 12 ;")
        grpName = name + "_grp"
        mc.group(name, n = grpName)
        return name, grpName
    
    def GetObjectLocation(self, objectName):
        x,y,z = mc.xform(objectName, q = True, ws = True, t = True) #aquires the translation of the object in world space
        return MVector(x,y,z)
    
    def PrintMVector(self, vector):
        print (f"<{vector.x}, {vector.y}, {vector.z}>")

    def RigLimb(self): #Definition for a function called RigLimb that has no parameters
        rootCtrl, rootCtrlGrp = self.CreateFKControllerForJoint(self.root) #sets rootCtrl and rootCtrlGrp to the return of CreakFKControllerForJoint passing self.root through
        midCtrl, midCtrlGrp = self.CreateFKControllerForJoint(self.mid) #sets midCtrl and midCtrlGrp to the return of CreakFKControllerForJoint passing self.mid through
        endCtrl, endCtrlGrp = self.CreateFKControllerForJoint(self.end) #sets endCtrl and endCtrlGrp to the return of CreakFKControllerForJoint passing self.end through

        mc.parent(midCtrlGrp, rootCtrl) #parents midCtrlGrp to rootCtrl
        mc.parent(endCtrlGrp, midCtrl) #parents endCtrlGrp to midCtrl

        ikEndCtrl = "ac_ik_" + self.end
        ikEndCtrl, ikEndCtrlGrp = self.CreateBoxController(ikEndCtrl)
        mc.matchTransform(ikEndCtrlGrp, self.end)
        endOrientConstraint = mc.orientConstraint(ikEndCtrl, self.end)[0]

        rootJntLoc = self.GetObjectLocation(self.root)
        self.PrintMVector(rootJntLoc)

        ikHandleName = "ikHandle_" + self.end
        mc.ikHandle(n = ikHandleName, sol = "ikRPsolver", sj = self.root, ee = self.end)

        poleVectorLocationVals = mc.getAttr(ikHandleName + ".poleVector")[0]
        poleVector = MVector(poleVectorLocationVals[0], poleVectorLocationVals[1], poleVectorLocationVals[2])
        poleVector.normalize()

        endJntLoc = self.GetObjectLocation(self.end)
        rootToEndVector = endJntLoc - rootJntLoc

        poleVectorCtrlLoc = rootJntLoc + rootToEndVector / 2 + poleVector * rootToEndVector.length()
        poleVectorCtrl = "ac_ik_" + self.mid
        mc.spaceLocator(n = poleVectorCtrl)
        poleVectorCtrlGrp = poleVectorCtrl + "_grp"
        mc.group(poleVectorCtrl, n = poleVectorCtrlGrp)
        mc.setAttr(poleVectorCtrlGrp + ".t", poleVectorCtrlLoc.x, poleVectorCtrlLoc.y, poleVectorCtrlLoc.z, typ = "double3")

        mc.poleVectorConstraint(poleVectorCtrl, ikHandleName)

        ikfkBlendCtrl = "ac_ikfk_blend_" + self.root
        ikfkBlendCtrl, ikfkBlendCtrlGrp = self.CreatePlusController(ikfkBlendCtrl)
        mc.setAttr(ikfkBlendCtrlGrp + ".t", rootJntLoc.x * 2, 0, rootJntLoc.z * 2, typ = "double3")
        mc.setAttr(ikfkBlendCtrlGrp + ".overrideEnabled", 1)
        mc.setAttr(ikfkBlendCtrlGrp + ".overrideColor", self.colorIndex)
 
        ikfkBelndAttrName = "ikfkBelnd"
        mc.addAttr(ikfkBlendCtrl, ln = ikfkBelndAttrName, min = 0, max = 1, k = True)
        ikfkBlendAttr = ikfkBlendCtrl + "." + ikfkBelndAttrName

        mc.expression(s = f"{ikHandleName}.ikBlend = {ikfkBlendAttr}")
        mc.expression(s = f"{ikEndCtrlGrp}.v = {poleVectorCtrlGrp}.v = {ikfkBlendAttr}")
        mc.expression(s =f"{rootCtrlGrp}.v = 1-{ikfkBlendAttr}")
        mc.expression(s = f"{endOrientConstraint}.{endCtrl}W0 = 1-{ikfkBlendAttr}")
        mc.expression(s = f"{endOrientConstraint}.{ikEndCtrl}W1 ={ikfkBlendAttr}")

        topGrpName = f"{self.root}_rig_grp"
        mc.group([rootCtrlGrp, ikEndCtrlGrp, poleVectorCtrlGrp, ikfkBlendCtrlGrp], n = topGrpName)

#######################################################
        mc.setAttr(topGrpName+ ".overrideEnabled", 1)
        mc.setAttr(topGrpName + ".overrideColor", self.colorIndex)
        mc.parent(ikHandleName, ikEndCtrl)
#######################################################

class LimbRiggerWidget(MayaWindow): #Definition for a class called LimbRiggerWidget that inherits from the MayaWindow class which inherits QWidget
    def __init__(self): #Definiton for the class contructor
        super().__init__() #Calls the contructor of the inherited class
        self.rigger = LimbRigger() #sets self.rigger to be a LimbRigger class

        self.masterLayout = QVBoxLayout() #sets self.masterLayout to be a QVBoxLayout class
        self.setLayout(self.masterLayout) #sets the layout of the widget to masterLayout

        self.setWindowTitle("Limb Rigger v1.0.0") #sets the widgets window title to LimbRigger

        toolTipLabel = QLabel("Select the first joint of the limb, and press the auto find button") #Sets toolTipLabel to a QLabel widget
        self.masterLayout.addWidget(toolTipLabel) #Adds the toolTipLabel widget to the masterLayout

        self.jntsListLineEdit = QLineEdit() #sets self.jntListLineEdit to be a QLineEdit widget
        self.masterLayout.addWidget(self.jntsListLineEdit) #Adds the jntsListLineEdit widget to the masterLayout
        self.jntsListLineEdit.setEnabled(False) #Disables the jntListLineEdit widget to it cant be typed on

        autoFindJntBtn = QPushButton("Auto Find") #sets autoFindJntBtn to be a QPushButton widget that says "Auto Find"
        autoFindJntBtn.clicked.connect(self.AutoFindJntBtnClicked) #when autoFindJntBtn is cliced it calls the AutoFindJntBtnClicked function
        self.masterLayout.addWidget(autoFindJntBtn) #adds the autoFindJntBtn widget to the masterLayout

        ctrlSizeSlider = QSlider() 
        ctrlSizeSlider.setOrientation(Qt.Horizontal)
        ctrlSizeSlider.setRange(1,30)
        ctrlSizeSlider.setValue(self.rigger.controllerSize)
        self.ctrlSizeLabel = QLabel(f"{self.rigger.controllerSize}")
        ctrlSizeSlider.valueChanged.connect(self.CtrlSizeSliderChanged)

        ctrlSizeLayout = QHBoxLayout()
        ctrlSizeLayout.addWidget(ctrlSizeSlider)
        ctrlSizeLayout.addWidget(self.ctrlSizeLabel)
        self.masterLayout.addLayout(ctrlSizeLayout)

#######################################################
        ctrlColorSlider = QSlider()
        ctrlColorSlider.setOrientation(Qt.Horizontal)
        ctrlColorSlider.setRange(1,31)
        ctrlColorSlider.setValue(self.rigger.colorIndex)
        self.ctrlColorLabel = QLabel()
        self.ctrlColorLabel.setFixedSize(50, 20)

        rgb = mc.colorIndex(self.rigger.colorIndex, q = True)
        rgb_str = f"rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})"
        self.ctrlColorLabel.setStyleSheet(f"background-color: {rgb_str}")
        
        ctrlColorSlider.valueChanged.connect(self.CtrlColorSliderChanged)

        ctrlColorLayout = QHBoxLayout()
        ctrlColorLayout.addWidget(ctrlColorSlider)
        ctrlColorLayout.addWidget(self.ctrlColorLabel)
        self.masterLayout.addLayout(ctrlColorLayout)
########################################################

        rigLimbBtn = QPushButton("Rig Limb") #sets rigLimbBtn to be a QPushButton widget that says "Rig Limb"
        rigLimbBtn.clicked.connect(lambda : self.rigger.RigLimb()) #when rigLimbBtn is clicked it calls a lambda function of RigLimb
        self.masterLayout.addWidget(rigLimbBtn) #adds the rigLimbBtn widget to the masterLayout

    def CtrlSizeSliderChanged(self, newValue):
        self.ctrlSizeLabel.setText(f"{newValue}")
        self.rigger.controllerSize = newValue

########################################################
    def CtrlColorSliderChanged(self, newValue):
        #self.ctrlColorLabel.setText(f"{newValue}")
        rgb = mc.colorIndex(newValue, q = True)
        rgb_str = f"rgb({int(rgb[0]*255)}, {int(rgb[1]*255)}, {int(rgb[2]*255)})"
        self.ctrlColorLabel.setStyleSheet(f"background-color: {rgb_str}")

        self.rigger.colorIndex = newValue
########################################################

    def AutoFindJntBtnClicked(self): #Definitoin for a function called AutoFindJntBtnClicked that has no parameters
        try: #The start of a try block
            self.rigger.FindJointsBasedOnSelection() #Calls the FindJintsBasedOnSelection function
            self.jntsListLineEdit.setText(f"{self.rigger.root}, {self.rigger.mid}, {self.rigger.end}") #sets the text of the QLineEdit widget to be the jnts that are selected
        except Exception as e: #the start of an except
            QMessageBox.critical(self, "Error", f"{e}") #Calls a window error if anything in the try block fails

limbRiggerWidget = LimbRiggerWidget() #sets limbRiggerWidget to be a LimbRiggerWidget class
limbRiggerWidget.show() #Shows the limbRiggerWidget on the Maya window

GetMayaMainWindow() #Calls the GetMayaWindow function