import os
import subprocess
import sys

from PySide6 import QtCore, QtGui, QtWidgets
from PySide6.QtWidgets import QFileDialog, QMessageBox
from PySide6.QtGui import QIcon, QTextCharFormat, QSyntaxHighlighter, QFont
from PySide6.QtCore import QRegularExpression, Qt

import ibdp_classes as ib


class BasicSyntaxHighlighter(QSyntaxHighlighter):
    def __init__(self, parent=None):
        super(BasicSyntaxHighlighter, self).__init__(parent)

        keywords_control_flow = [
            "if",
            "else",
            "else if",
            "end",
            "while",
            "loop",
            "to",
            "until",
            "then",
        ]
        keywords_data_structures = [
            "Collection",
            "Array",
            "Stack",
            "Queue",
            "isEmpty()",
            "hasNext()",
            "resetNext()",
            "getNext()",
            "addItem",
            "push",
            "pop",
            "dequeue",
            "enqueue",
        ]
        keywords_boolean_logic = ["true", "false", "not"]
        keywords_comparison = ["<", "=", ">", "//", "!"]
        keywords_procedures = ["procedure", "end procedure", "function", "end function"]
        keywords_io = ["new", "output", "input"]

        # Define colors and formats for each category
        control_flow_format = QTextCharFormat()
        control_flow_format.setForeground(Qt.darkCyan)
        control_flow_format.setFontWeight(QFont.Normal)

        data_structures_format = QTextCharFormat()
        data_structures_format.setForeground(Qt.darkGreen)
        data_structures_format.setFontWeight(QFont.Normal)

        boolean_logic_format = QTextCharFormat()
        boolean_logic_format.setForeground(Qt.darkMagenta)
        boolean_logic_format.setFontWeight(QFont.Normal)

        comparison_format = QTextCharFormat()
        comparison_format.setForeground(Qt.darkGray)
        comparison_format.setFontWeight(QFont.Normal)

        procedures_format = QTextCharFormat()
        procedures_format.setForeground(Qt.darkYellow)
        procedures_format.setFontWeight(QFont.Normal)

        io_format = QTextCharFormat()
        io_format.setForeground(Qt.red)
        io_format.setFontWeight(QFont.Normal)

        self.highlightingRules = (
            [
                (QRegularExpression(r"\b" + keyword + r"\b"), control_flow_format)
                for keyword in keywords_control_flow
            ]
            + [
                (QRegularExpression(r"\b" + keyword + r"\b"), data_structures_format)
                for keyword in keywords_data_structures
            ]
            + [
                (QRegularExpression(r"\b" + keyword + r"\b"), boolean_logic_format)
                for keyword in keywords_boolean_logic
            ]
            + [
                (QRegularExpression(r"\b" + keyword + r"\b"), comparison_format)
                for keyword in keywords_comparison
            ]
            + [
                (QRegularExpression(r"\b" + keyword + r"\b"), procedures_format)
                for keyword in keywords_procedures
            ]
            + [
                (QRegularExpression(r"\b" + keyword + r"\b"), io_format)
                for keyword in keywords_io
            ]
        )

    def highlightBlock(self, text):
        for pattern, format in self.highlightingRules:
            expression = QRegularExpression(pattern)
            match = expression.match(text)
            while match.hasMatch():
                start = match.capturedStart()
                length = match.capturedLength()
                self.setFormat(start, length, format)
                match = expression.match(text, start + length)


# UI definition using Qt Designer-generated code
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
        MainWindow.setWindowIcon(QIcon("ui/icons/icon.svg"))
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
        self.actionSave = QtGui.QAction(MainWindow)
        self.actionSave.setObjectName("actionSave")
        self.actionSave_AS = QtGui.QAction(MainWindow)
        self.actionSave_AS.setObjectName("actionSave_AS")
        self.actionOpen = QtGui.QAction(MainWindow)
        self.actionOpen.setObjectName("actionOpen")
        self.actionExecute = QtGui.QAction(MainWindow)
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
        
        self.highlighter = BasicSyntaxHighlighter(self.textEdit.document())

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
            file_path = f"{file_name}.ib.bas"

        with open(file_path, "w") as file:
            file.write(self.textEdit.toPlainText())
        self.file_path = file_path

    def save_file_as(self):
        file_path, _ = QFileDialog.getSaveFileName(None, "Save File As", "", "*.ib.bas")
        if file_path:
            file_name = os.path.splitext(os.path.basename(file_path))[
                0
            ]
            file_path = f"{file_name}.ib.bas"
            with open(file_path, "w") as file:
                file.write(self.textEdit.toPlainText())
            self.file_path = file_path

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(None, "Open File", "", "*.ib.bas")
        if file_path:
            self.file_path = file_path
            with open(self.file_path, "r") as file:
                content = file.read()
                self.textEdit.setPlainText(content)

    def execute_code(self):
        code = self.textEdit.toPlainText()
        try:
            file_name = ".temp.ib.bas"

            # Save the code to the temporary file
            with open(file_name, "w") as file:
                file.write(code)

            # Run the ibdp_classes module with the temporary file
            cmd = f"python -m ibdp_classes {file_name}"
            try:
                # Check the operating system
                if os.name == "nt":  # Windows
                    subprocess.run(f'start cmd /k "{cmd}"', shell=True, check=True)
                elif os.name == "posix":  # Linux or MacOS
                    term_program = os.getenv("TERM")
                    if term_program == "Apple_Terminal":  # MacOS
                        subprocess.run(
                            f'open -a Terminal "{cmd}"', shell=True, check=True
                        )
                    else:
                        subprocess.run(f"$TERM --hold -e {cmd}", shell=True, check=True)
                else:
                    print(
                        "Unsupported operating system. If you're on a POSIX system, you need to setup the $TERM environment variable to your terminal emulator"
                    )
            except subprocess.CalledProcessError as e:
                print(f"Error: {e}")

        except Exception as e:
            print(f"Error: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())
