import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
import ibdp_classes as ib
import subprocess

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("CodeNewRoman Nerd Font")
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textEdit = QtWidgets.QTextEdit(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(
            QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding
        )
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.textEdit.sizePolicy().hasHeightForWidth())
        self.textEdit.setSizePolicy(sizePolicy)
        self.textEdit.setObjectName("textEdit")
        self.gridLayout_2.addWidget(self.textEdit, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 29))
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        self.menuFile.setObjectName("menuFile")
        self.menuExecute = QtWidgets.QMenu(self.menubar)
        self.menuExecute.setObjectName("menuExecute")
        MainWindow.setMenuBar(self.menubar)
        self.actionSave = QtWidgets.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_AS = QtWidgets.QAction(MainWindow)
        self.actionSave_AS.setObjectName("actionSave_AS")
        self.actionOpen = QtWidgets.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExecute = QtWidgets.QAction(MainWindow)
        self.actionExecute.setObjectName("actionExecute")
        self.menuFile.addAction(self.actionSave)
        self.menuFile.addAction(self.actionSave_AS)
        self.menuFile.addAction(self.actionOpen)
        self.menuExecute.addAction(self.actionExecute)
        self.menubar.addAction(self.menuFile.menuAction())
        self.menubar.addAction(self.menuExecute.menuAction())

        self.actionSave.triggered.connect(self.save_file)
        self.actionSave_AS.triggered.connect(self.save_file_as)
        self.actionOpen.triggered.connect(self.open_file)
        self.actionExecute.triggered.connect(self.execute_code)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "codeDP-IB Pseudocode"))
        self.menuFile.setTitle(_translate("MainWindow", "File"))
        self.menuExecute.setTitle(_translate("MainWindow", "Code"))
        self.actionSave.setText(_translate("MainWindow", "Save "))
        self.actionSave.setShortcut(_translate("MainWindow", "Ctrl+S"))
        self.actionSave_AS.setText(_translate("MainWindow", "Save As"))
        self.actionSave_AS.setShortcut(_translate("MainWindow", "Ctrl+Shift+S"))
        self.actionOpen.setText(_translate("MainWindow", "Open"))
        self.actionOpen.setShortcut(_translate("MainWindow", "Ctrl+O"))
        self.actionExecute.setText(_translate("MainWindow", "Execute"))
        self.actionExecute.setShortcut(_translate("MainWindow", "Ctrl+Return"))

    def save_file(self):
        if hasattr(self, "file_path") and self.file_path:
            file_path = self.file_path
        else:
            file_path, _ = QFileDialog.getSaveFileName(
                None, "Save File", "", "*.ib.bas"
            )
            if not file_path:
                return  # User canceled the save operation, do nothing
            file_name = os.path.splitext(os.path.basename(file_path))[
                0
            ]  # Extract filename without extension
            file_path = f"{file_name}.ib.bas"  # Append .ib.bas extension

        with open(file_path, "w") as file:
            file.write(self.textEdit.toPlainText())
        self.file_path = file_path  # Update the current file path

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "Save File As", "", "*.ib.bas")
        if file_path:
            file_name = os.path.splitext(os.path.basename(file_path))[
                0
            ]  # Extract filename without extension
            file_path = f"{file_name}.ib.bas"  # Append .ib.bas extension
            with open(file_path, "w") as file:
                file.write(self.textEdit.toPlainText())
            self.file_path = file_path  # Update the current file path

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "*.ib.bas")
        if file_path:
            self.file_path = file_path
            with open(self.file_path, "r") as file:
                content = file.read()
                self.textEdit.setPlainText(content)

    def execute_code(self):
        """
        Run the saved code in a console instance similar to how vscode/pycharm runs code in an integrated terminal
        """
        code = self.textEdit.toPlainText()
        try:
            script = ib.Pseudocode(code)
            print(script())
        except Exception as e:
            print(f"Error: {e}")
