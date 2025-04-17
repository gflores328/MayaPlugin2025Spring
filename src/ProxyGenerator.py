import importlib
import MayaUtils
importlib.reload(MayaUtils)

from MayaUtils import GetAllConnectionsIn, GetUpperStream, IsJoint, IsMesh, IsSkin, MayaWindow
from PySide2.QtWidgets import QLabel, QPushButton, QVBoxLayout
import maya.cmds as mc

class ProxyGenerator:
    def __init__(self):
        self.skin = ""
        self.model = ""
        self.jnts = []

    def BuildProxyForSelectedMesh(self):
        model = mc.ls(sl = True)[0]
        if not IsMesh(model):
            print (f"{model} is not a mesh")
            return
        
        self.model = model
        print (f"found model {self.model}")
        modelShape = mc.listRelatives(self.model, s = True)[0]
        skin = GetAllConnectionsIn(modelShape, GetUpperStream, IsSkin)
        if not skin:
            print (f"{self.model} is not bound!")
            return
        jnts = GetAllConnectionsIn(modelShape, GetUpperStream, IsJoint)
        if not jnts:
            print(f"{self.model} is not bound with any joint!")
            return
        
        self.skin = skin[0]
        self.jnts = jnts
        print (f"found model {self.model} with skin {self.skin} and  joints: {self.jnts}")
        
        jntVertDict = self.GenerateJntVertsDict()
        chunks = []
        ctrls = []
        for jnt, verts in jntVertDict.items():
            print(f"joint {jnt} controls {verts}")
            newChunk = self.CreateProxyModelForJntAndVerts(jnt, verts)
            if not newChunk:
                continue

            newSkinCluster = mc.skinCluster(self.jnts, newChunk)[0]
            mc.copySkinWeights(ss = self.skin, ds = newSkinCluster, nm = True, sa = "closestPoint", ia = "closestJoint")
            chunks.append(newChunk)

            ctrlName = "ac_" + jnt + "_proxy"
            mc.spaceLocator(n = ctrlName)
            ctrlGrpName = ctrlName + "_grp"
            mc.group(ctrlName, n = ctrlGrpName)
            mc.matchTransform(ctrlGrpName, jnt)

            visibilityAttr = "vis"
            mc.addAttr(ctrlName, ln = visibilityAttr, min = 0, max = 1, dv = 1, k = True)
            mc.connectAttr(ctrlName + "." + visibilityAttr, newChunk + ".v")
            ctrls.append(ctrlGrpName)

        proxyTopGroup = self.model + "_proxy_grp"
        mc.group(chunks, n = proxyTopGroup)

        ctrlTopGrp = "ac_" + self.model + "_proxy_grp"
        mc.group(ctrls, n = ctrlTopGrp)

        globalProxyCtrl = "ac_" + self.model + "_proxy_global"
        mc.circle(n = globalProxyCtrl, r = 20)

        mc.parent(proxyTopGroup, globalProxyCtrl)
        mc.parent(ctrlTopGrp, globalProxyCtrl)

        mc.setAttr(proxyTopGroup + ".inheritsTransform", 0)

        mc.addAttr(globalProxyCtrl, ln = "vis", min = 0, max = 1, k = True, dv = 1)
        mc.connectAttr(globalProxyCtrl + ".vis", proxyTopGroup + ".v")

    def CreateProxyModelForJntAndVerts(self, jnt, verts):
        if not verts:
            return None
        
        faces = mc.polyListComponentConversion(verts, fromVertex = True, toFace = True)
        faces = mc.ls(faces, fl = True)

        faceNames = set()
        for face in faces:
            faceNames.add(face.replace(self.model, ""))

        dup = mc.duplicate(self.model)[0]
        allDupFaces = mc.ls(f"{dup}.f[*]", fl = True)
        facesToDelete = []
        for dupFace in allDupFaces:
            if dupFace.replace(dup, "") not in faceNames:
                facesToDelete.append(dupFace)

        mc.delete(facesToDelete)
        dupName = self.model + "_" + jnt + "_proxy"
        mc.rename(dup, dupName)
        return dupName


    def GenerateJntVertsDict(self):
        dict = {}
        for jnt in self.jnts:
            dict[jnt] = []

        verts = mc.ls(f"{self.model}.vtx[*]", fl = True)
        for vert in verts:
            owningJnt = self.GetJntWithMaxInfluence(vert, self.skin)
            dict[owningJnt].append(vert)

        return dict


    def GetJntWithMaxInfluence(self, vert, skin):
        weights = mc.skinPercent(skin, vert, q = True, v = True)
        jnts = mc.skinPercent(skin, vert, q = True, t = None)

        maxWeightIndex = 0
        maxWeight = weights[0]
        for i in range(1, len(weights)):
            if weights[i] > maxWeight:
                maxWeight = weights[i]
                maxWeightIndex = i

        return jnts[maxWeightIndex]

class ProxyGeneratorWidget(MayaWindow):
    def __init__(self):
        super().__init__()
        self.generator = ProxyGenerator()
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        self.masterLayout.addWidget(QLabel("Please select the rigged model, and press the build button"))
        buildBtn = QPushButton("Build")
        self.masterLayout.addWidget(buildBtn)
        buildBtn.clicked.connect(self.generator.BuildProxyForSelectedMesh)

    def GetWindowUniqueName(self):
        return "ProxyGeneratorGF14122025212"
    
ProxyGeneratorWidget().show()