from PySide6 import QtCore

from assets import board

pieceNumber = 1

class AppFunctions(QtCore.QObject):
    # Request Signals
    updateViewportRequest = QtCore.Signal()
    newPieceAdded = QtCore.Signal()
    pieceNumber = 1

    def __init__(self):
        super(AppFunctions, self).__init__()
        self.model = None
        self.viewportWidget = None

    def setModel(self, model):
        self.model = model

    def getModel(self):
        return self.model

    def setViewportWidget(self, viewport):
        self.viewportWidget = viewport

    def getViewportWidget(self):
        return self.viewportWidget

    def getSceneStage(self):
        return self.model.stage

    def updateViewport(self):
        self.updateViewportRequest.emit()

    def createNewPiece(self):
        testBored = board.Board('board{}'.format(str(self.pieceNumber)), 1200, 2400, 16, self)
        self.pieceNumber = self.pieceNumber + 1

        self.viewportWidget.updateView()
        self.newPieceAdded.emit()
        print('create new piece')