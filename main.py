import sys
from PySide6 import QtWidgets, QtGui, QtCore

from pxr import Usd, UsdUtils, Sdf, UsdGeom, Gf
from pxr.Usdviewq.stageView import StageView

from appFunctions import functions
from assets import board
from panels.hydra import viewport
from panels.sceneGraph import sceneGraph
from styleSheets import uiStyleSheet
from widgets import mainMenuBar
app = QtWidgets.QApplication([])


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, defaultStage=None):
        super().__init__()

        # Main Window Setup
        self.setWindowTitle("Dale")
        self.setGeometry(100, 100, 800, 600)

        # End menu bar and set up workspace
        self.appFunctions = functions.AppFunctions()
        self.appFunctions.setModel(StageView.DefaultDataModel())

        mainMenuBar.SetUpMenuBar(self, self.appFunctions)

        if defaultStage:
            self.appFunctions.model.stage = defaultStage
        else:
            self.appFunctions.model.stage = Usd.Stage.CreateNew("sceneStage.usda")

        #testBored = board.Board('board1', 1200, 2400, 16, self.appFunctions)

        # Dockable viewport
        viewer = viewport.HydraViewer(appFunctions=self.appFunctions)
        self.addDockWidget(QtCore.Qt.RightDockWidgetArea, viewer)

        # Dockable Scenegraph
        sceneTree = sceneGraph.Scenegraph(appFunctions=self.appFunctions)
        sceneTree.setMaximumWidth(350)
        self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, sceneTree)

        # Docking Behavior
        viewer.setFloating(False)  # Ensure dock starts docked

        self.setStyleSheet(uiStyleSheet.styleSheet)

if __name__ == "__main__":
    stage = None
    #with Usd.StageCacheContext(UsdUtils.StageCache.Get()):
    #    stage = Usd.Stage.Open(USD_FILE_PATH)

    mainWindow = MainWindow(defaultStage=None)
    mainWindow.setWindowTitle("DALE")
    mainWindow.resize(QtCore.QSize(750, 750))
    mainWindow.show()

    app.exec()