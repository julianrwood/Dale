import sys

from PySide6 import QtWidgets, QtGui, QtCore

from pxr import Usd, UsdUtils, Sdf, UsdGeom, Gf, UsdShade
from pxr.Usdviewq.stageView import StageView


class transformMaterials:
    def __init__(self, stage):
        self.xMaterial = None
        self.yMaterial = None
        self.zMaterial = None
        self.highLightMaterial = None

        self.stage = stage

        self.createTransformxMaterial()
        self.createTransformyMaterial()
        self.createTransformzMaterial()
        self.createHighLightMaterial()

    def createTransformxMaterial(self):
        # Define the material
        material = UsdShade.Material.Define(self.stage, '/materials/transformMaterials/xMat')

        # Define the shader within the material
        shader = UsdShade.Shader.Define(self.stage, material.GetPath().AppendChild("xShader"))
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set the diffuse color input
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 0.0, 0.0))
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

        self.xMaterial = material

    def createTransformyMaterial(self):
        # Define the material
        material = UsdShade.Material.Define(self.stage, '/materials/transformMaterials/yMat')

        # Define the shader within the material
        shader = UsdShade.Shader.Define(self.stage, material.GetPath().AppendChild("yShader"))
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set the diffuse color input
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.0, 1.0, 0.0))
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

        self.yMaterial = material

    def createTransformzMaterial(self):
        # Define the material
        material = UsdShade.Material.Define(self.stage, '/materials/transformMaterials/zMat')

        # Define the shader within the material
        shader = UsdShade.Shader.Define(self.stage, material.GetPath().AppendChild("zShader"))
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set the diffuse color input
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((0.0, 0.0, 1.0))
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

        self.zMaterial = material

    def createHighLightMaterial(self):
        # Define the material
        material = UsdShade.Material.Define(self.stage, '/materials/transformMaterials/highMat')

        # Define the shader within the material
        shader = UsdShade.Shader.Define(self.stage, material.GetPath().AppendChild("highlightShader"))
        shader.CreateIdAttr("UsdPreviewSurface")

        # Set the diffuse color input
        shader.CreateInput("diffuseColor", Sdf.ValueTypeNames.Color3f).Set((1.0, 1.0, 0.0))  # Yellow color (1.0, 1.0, 0.0)
        material.CreateSurfaceOutput().ConnectToSource(shader.ConnectableAPI(), "surface")

        self.highLightMaterial = material


class CreateArrows:
    def __init__(self, stage, basePath, axis, materials, arrowLength=220, arrowRadius=8, coneHeight=50, coneRadius=18):
        """
        Create an arrow aligned to the specified axis and set bounding boxes.

        Args:
            stage: The USD stage.
            basePath: The base SdfPath where the arrow will be created.
            axis: The axis ('X', 'Y', or 'Z') along which the arrow will align.
            arrowLength: Length of the arrow shaft.
            arrowRadius: Radius of the arrow shaft.
            coneHeight: Height of the arrow cone.
            coneRadius: Radius of the arrow cone.
        """
        self.stage = stage
        self.basePath = basePath
        self.axis = axis
        self.materials = materials
        self.arrowLength = arrowLength
        self.arrowRadius = arrowRadius
        self.coneHeight = coneHeight
        self.coneRadius =coneRadius

        self.prims = []

        axies = ['X', 'Y', 'Z']

        for axis in axies:
            self.createArrow(axis)

    def createArrow(self, axis):
        arrowPath = self.basePath.AppendChild(f"{axis}_AxisArrow")
        arrowXform = UsdGeom.Xform.Define(self.stage, arrowPath)

        # Create the cylinder (shaft)
        cylinder = UsdGeom.Cylinder.Define(self.stage, arrowPath.AppendChild("Cylinder"))
        cylinder.GetHeightAttr().Set(self.arrowLength)
        cylinder.GetRadiusAttr().Set(self.arrowRadius)

        # Set the bounding box for the cylinder
        cylinderExtent = [
            (-self.arrowRadius, -self.arrowRadius, 0),
            (self.arrowRadius, self.arrowRadius, self.arrowLength),
        ]
        cylinder.GetExtentAttr().Set(cylinderExtent)

        # Create the cone (tip)
        cone = UsdGeom.Cone.Define(self.stage, arrowPath.AppendChild("Cone"))
        cone.GetHeightAttr().Set(self.coneHeight)
        cone.GetRadiusAttr().Set(self.coneRadius)

        # Set the bounding box for the cone
        coneExtent = [
            (-self.coneRadius, -self.coneRadius, 0),
            (self.coneRadius, self.coneRadius, self.coneHeight),
        ]
        cone.GetExtentAttr().Set(coneExtent)

        # Position the cone at the end of the cylinder
        coneOffset = self.arrowLength

        # Initial material setup
        conePrim = cone.GetPrim()
        conePrim.ApplyAPI(UsdShade.MaterialBindingAPI)
        cylinderPrim = cylinder.GetPrim()
        cylinderPrim.ApplyAPI(UsdShade.MaterialBindingAPI)

        # Translate and rotate based on axis
        if axis == 'X':
            cylinder.AddTranslateOp().Set((0, 0, self.arrowLength / 2))
            cone.AddTranslateOp().Set((0, 0, coneOffset))
            UsdShade.MaterialBindingAPI(cylinderPrim).Bind(self.materials.xMaterial)
            UsdShade.MaterialBindingAPI(conePrim).Bind(self.materials.xMaterial)
        elif axis == 'Y':
            cylinder.AddTranslateOp().Set((0, self.arrowLength / 2, 0))
            cone.AddTranslateOp().Set((0, coneOffset, 0))

            cylinder.AddRotateXYZOp().Set((90, 0, 0))
            cone.AddRotateXYZOp().Set((270, 0, 0))

            UsdShade.MaterialBindingAPI(cylinderPrim).Bind(self.materials.yMaterial)
            UsdShade.MaterialBindingAPI(conePrim).Bind(self.materials.yMaterial)

        elif axis == 'Z':
            cylinder.AddTranslateOp().Set((self.arrowLength / 2, 0, 0))
            cone.AddTranslateOp().Set((coneOffset, 0, 0))

            cylinder.AddRotateXYZOp().Set((0, 270, 0))
            cone.AddRotateXYZOp().Set((0, 90, 0))
            UsdShade.MaterialBindingAPI(cylinderPrim).Bind(self.materials.zMaterial)
            UsdShade.MaterialBindingAPI(conePrim).Bind(self.materials.zMaterial)

        self.prims.append(cylinderPrim)
        self.prims.append(conePrim)

class HydraViewer(QtWidgets.QDockWidget):
    def __init__(self, appFunctions):
        super(HydraViewer, self).__init__('Hydra Viewport')
        self.appFunctions = appFunctions
        self.selectedPrim = None
        self.transformArrows = None

        # Initiate the Hydra viewer
        self.view = StageView(dataModel=self.appFunctions.model)
        self.view.rolloverPicking = True
        self.appFunctions.setViewportWidget(self.view)
        self.setWidget(self.view)

        self.transformMaterials = transformMaterials(self.appFunctions.model.stage)

        # Connect selection changes
        self.view.signalPrimSelected.connect(self.onPrimSelected)
        self.view.signalPrimRollover.connect(self.signalPrimRollover)

        # Create transform controls
        self.createTransformHandle()

    def onPrimSelected(self, primPath):
        stage = self.appFunctions.model.stage
        if stage:
            self.selectedPrim = stage.GetPrimAtPath(primPath)
            if primPath.name.split('/')[-1] in ['Cylinder', 'Cone']:
                return

            print(f"Selected Prim: {self.selectedPrim.GetPath()}")
            self.createTransformHandle()

    def createTransformHandle(self):
        if not self.selectedPrim:
            return

        # Create a visual handle at the selected prim's position
        handlePath = self.selectedPrim.GetPath().AppendChild("TransformHandle")
        stage = self.appFunctions.model.stage
        handlePrim = UsdGeom.Xform.Define(stage, handlePath)

        # Create a visual handle at the selected prim's position
        handlePath = self.selectedPrim.GetPath().AppendChild("TransformHandle")
        stage = self.appFunctions.model.stage
        UsdGeom.Xform.Define(stage, handlePath)  # Root transform handle

        # Create arrows for X, Y, and Z axes
        self.transformArrows = CreateArrows(stage, handlePath, 'X', self.transformMaterials)

        # Update the viewport
        self.view.updateView()

    def applyTransform(self, translate=(0, 0, 0), rotate=(0, 0, 0), scale=(1, 1, 1)):
        if not self.selectedPrim:
            print("No geometry selected.")
            return

        xform = UsdGeom.Xform(self.selectedPrim)
        if not xform:
            print(f"Selected Prim is not transformable: {self.selectedPrim.GetPath()}")
            return

        translateOp = xform.AddTranslateOp()
        translateOp.Set(translate)

        rotateOp = xform.AddRotateXYZOp()
        rotateOp.Set(rotate)

        scaleOp = xform.AddScaleOp()
        scaleOp.Set(scale)

        self.updateViewPort()

    def signalPrimRollover(self, selectedPrimPath, selectedInstanceIndex, selectedTLPath,
                    selectedTLIndex, selectedPoint, modifiers):
        """
        Handle hover and drag events.
        """
        if selectedPrimPath.name.split('/')[-1] in ['Cylinder', 'Cone']:
            prim = self.appFunctions.model.stage.GetPrimAtPath(selectedPrimPath)
            UsdShade.MaterialBindingAPI(prim).Bind(self.transformMaterials.highLightMaterial)

            self.view.updateView()

        return

