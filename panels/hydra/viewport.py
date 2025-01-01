import sys

from PySide6 import QtWidgets, QtGui, QtCore

from pxr import Usd, UsdUtils, Sdf, UsdGeom
from pxr.Usdviewq.stageView import StageView


def create_arrow(stage, basePath, axis, arrowLength=300, arrowRadius=10, coneHeight=50, coneRadius=20):
    """
    Create an arrow aligned to the specified axis.

    Args:
        stage: The USD stage.
        basePath: The base SdfPath where the arrow will be created.
        axis: The axis ('X', 'Y', or 'Z') along which the arrow will align.
        arrowLength: Length of the arrow shaft.
        arrowRadius: Radius of the arrow shaft.
        coneHeight: Height of the arrow cone.
        coneRadius: Radius of the arrow cone.
    """
    arrowPath = basePath.AppendChild(f"{axis}_AxisArrow")
    arrowXform = UsdGeom.Xform.Define(stage, arrowPath)

    # Create the cylinder (shaft)
    cylinder = UsdGeom.Cylinder.Define(stage, arrowPath.AppendChild("Cylinder"))
    cylinder.GetHeightAttr().Set(arrowLength)
    cylinder.GetRadiusAttr().Set(arrowRadius)

    # Create the cone (tip)
    cone = UsdGeom.Cone.Define(stage, arrowPath.AppendChild("Cone"))
    cone.GetHeightAttr().Set(coneHeight)
    cone.GetRadiusAttr().Set(coneRadius)

    # Position the cone at the end of the cylinder
    coneOffset = arrowLength

    # Translate and rotate based on axis
    if axis == 'X':
        cylinder.AddTranslateOp().Set((0, 0, arrowLength/2))
        cone.AddTranslateOp().Set((0, 0, coneOffset))
    elif axis == 'Y':
        cylinder.AddTranslateOp().Set((0, arrowLength/2, 0))
        cone.AddTranslateOp().Set((0, coneOffset, 0))

        cylinder.AddRotateXYZOp().Set((90, 0, 0))
        cone.AddRotateXYZOp().Set((270, 0, 0))
    elif axis == 'Z':
        cylinder.AddTranslateOp().Set((arrowLength/2, 0, 0))
        cone.AddTranslateOp().Set((coneOffset, 0, 0))

        cylinder.AddRotateXYZOp().Set((0, 270, 0))
        cone.AddRotateXYZOp().Set((0, 90, 0))

    return arrowPath


class HydraViewer(QtWidgets.QDockWidget):
    def __init__(self, appFunctions):
        super(HydraViewer, self).__init__('Hydra Viewport')
        self.appFunctions = appFunctions
        self.selectedPrim = None

        # Initiate the Hydra viewer
        self.view = StageView(dataModel=self.appFunctions.model)
        self.appFunctions.setViewportWidget(self.view)
        self.setWidget(self.view)

        # Connect selection changes
        self.view.signalPrimSelected.connect(self.onPrimSelected)

        # Create transform controls
        self.createTransformHandle()

    def onPrimSelected(self, primPath):
        stage = self.appFunctions.model.stage
        if stage:
            self.selectedPrim = stage.GetPrimAtPath(primPath)
            print(dir(primPath))
            if primPath.name.split('/')[-1] in ['Cylinder' or 'Cone']:
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
        create_arrow(stage, handlePath, 'X')
        create_arrow(stage, handlePath, 'Y')
        create_arrow(stage, handlePath, 'Z')

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
