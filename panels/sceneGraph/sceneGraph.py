from PySide6 import QtWidgets, QtGui, QtCore


class TreeItem(QtGui.QStandardItem):
    def __init__(self, name):
        super(TreeItem, self).__init__(name)


class TreeModel(QtGui.QStandardItemModel):
    def __init__(self, appFunctions):
        super(TreeModel, self).__init__()
        self.appFunctions = appFunctions
        self.appFunctions.newPieceAdded.connect(self.appendModel)
        self.rootItem = None

        # Populate the model
        self.populateModel()

    def traverseChildren(self, parentItem, parentPrim):
        children = parentPrim.GetChildren()
        for child in children:
            item = TreeItem(child.GetName())
            parentItem.appendRow(item)

            self.traverseChildren(item, child)

    def appendModel(self):
        # clear the model
        self.clear()

        # Set headers
        self.setHorizontalHeaderLabels(["Scene Item List"])
        self.rootItem = TreeItem('root')
        self.invisibleRootItem().appendRow(self.rootItem)

        # Get stage
        stage = self.appFunctions.getSceneStage()

        # Get the root prim
        rootPrim = stage.GetPseudoRoot()

        # Get only the immediate children (one level deep)
        for child in rootPrim.GetChildren():
            item = TreeItem(child.GetName())
            self.rootItem.appendRow(item)
            self.traverseChildren(item, child)

    def populateModel(self):
        # begin population of the model
        self.rootItem = self.invisibleRootItem().appendRow(TreeItem('root'))


class TreeView(QtWidgets.QTreeView):
    def __init__(self, model):
        super(TreeView, self).__init__()
        self.setModel(model)

        # Enable column resizing
        self.header().setStretchLastSection(True)

        # Expand all rows initially
        self.expandAll()

class Scenegraph(QtWidgets.QDockWidget):
    def __init__(self, appFunctions):
        super(Scenegraph, self).__init__('Scene Graph')
        self.appFunctions = appFunctions
        self.model = TreeModel(self.appFunctions)
        self.treeView = TreeView(self.model)

        # When a new piece is added we fully expand the sceneGraph, this is for debugging and will be removed
        self.appFunctions.newPieceAdded.connect(self.treeView.expandAll)

        self.setWidget(self.treeView)

