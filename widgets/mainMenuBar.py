from PySide6 import QtGui

class SetUpMenuBar:
    def __init__(self, mainWindow, appFunctions):

        menu_bar = mainWindow.menuBar()

        # Create menus
        fileMenu = menu_bar.addMenu("File")
        editMenu = menu_bar.addMenu("Edit")
        createMenu = menu_bar.addMenu("Create")
        helpMenu = menu_bar.addMenu("Help")

        # Add actions to the "File" menu
        newAction = QtGui.QAction("New", mainWindow)
        openAction = QtGui.QAction("Open", mainWindow)
        saveAction = QtGui.QAction("Save", mainWindow)
        exitAction = QtGui.QAction("Exit", mainWindow)

        fileMenu.addAction(newAction)
        fileMenu.addAction(openAction)
        fileMenu.addAction(saveAction)
        fileMenu.addSeparator()
        fileMenu.addAction(exitAction)

        # Add actions to the "Edit" menu
        cutAction = QtGui.QAction("Cut", mainWindow)
        copyAction = QtGui.QAction("Copy", mainWindow)
        pasteAction = QtGui.QAction("Paste", mainWindow)

        editMenu.addAction(cutAction)
        editMenu.addAction(copyAction)
        editMenu.addAction(pasteAction)

        # Add actions to the create menu
        createPiece = QtGui.QAction("Create Piece", mainWindow)

        createPiece.triggered.connect(appFunctions.createNewPiece)

        createMenu.addAction(createPiece)

        # Add actions to the "Help" menu
        about_action = QtGui.QAction("About", mainWindow)
        helpMenu.addAction(about_action)

        # Connect actions to methods
        exitAction.triggered.connect(mainWindow.close)