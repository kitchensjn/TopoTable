"""
PyQt Graphical User Interface

James Kitchens - 08/31/2019

Frontend of the map conversion. This code communicates with the backend program used to take maps downloaded from 'terrain.party'
and produce a .csv file with associated heights of each pillar to display map to scale. Running this code opens a new window with
inputs used to set parameters for backend.
"""

import sys
import pixelateAndScaleMap
from PyQt5 import QtWidgets


helpDialog = """Help Dialog\n
Folder: the path to the directory which contains the desired maps and README.txt\n
Footprint: taken from terrain.party, the size of one dimension of the square in meters (8km x 8km = 8000). Leave off units!\n
PillarNumber: the number of pillars which make up one dimension of the table (100pillars x 100pillars = 100)\n
PillarSize: the size of one dimension of an individual pillar (length or width), generally 1. Leave off units!\n
"""                                                                                                                                                                                             # Help dialog text explaining each entry dialog

class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.folderLabel = QtWidgets.QLabel('Folder')                                                                                                                                           # Sets up the labels for each entry dialog
        self.folderEntry = QtWidgets.QLineEdit()
        self.footprintLabel = QtWidgets.QLabel('Footprint')
        self.footprintEntry = QtWidgets.QLineEdit()
        self.pixelNumberLabel = QtWidgets.QLabel('PillarNumber')
        self.pixelNumberEntry = QtWidgets.QLineEdit()
        self.pixelSizeLabel = QtWidgets.QLabel('PillarSize')
        self.pixelSizeEntry = QtWidgets.QLineEdit()
        self.browseButton = QtWidgets.QPushButton('Browse')
        self.clearButton = QtWidgets.QPushButton('Clear')
        self.printButton = QtWidgets.QPushButton('Run')
        self.message = QtWidgets.QLabel('')
        self.helpButton = QtWidgets.QPushButton('Help')

        h_box1 = QtWidgets.QHBoxLayout()                                                                                                                                                        # Creates folder entry dialog
        h_box1.addWidget(self.folderLabel)
        h_box1.addWidget(self.folderEntry)
        h_box1.addWidget(self.browseButton)

        h_box2 = QtWidgets.QHBoxLayout()                                                                                                                                                        # Creates footprint entry dialog
        h_box2.addWidget(self.footprintLabel)
        h_box2.addWidget(self.footprintEntry)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addWidget(self.pixelNumberLabel)
        h_box3.addWidget(self.pixelNumberEntry)

        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addWidget(self.pixelSizeLabel)
        h_box4.addWidget(self.pixelSizeEntry)

        h_box5 = QtWidgets.QHBoxLayout()
        h_box5.addWidget(self.printButton)
        h_box5.addWidget(self.clearButton)

        h_box6 = QtWidgets.QHBoxLayout()
        h_box6.addStretch()
        h_box6.addWidget(self.message)
        h_box6.addStretch()

        h_box7 = QtWidgets.QHBoxLayout()
        h_box7.addStretch()
        h_box7.addWidget(self.helpButton)

        v_box = QtWidgets.QVBoxLayout()                                                                                                                                                         # Sets layout and order of dialogs
        v_box.addLayout(h_box1)
        v_box.addLayout(h_box2)
        v_box.addLayout(h_box3)
        v_box.addLayout(h_box4)
        v_box.addLayout(h_box5)
        v_box.addLayout(h_box6)
        v_box.addLayout(h_box7)

        self.setLayout(v_box)

        self.browseButton.clicked.connect(self.btn_click)
        self.clearButton.clicked.connect(self.btn_click)
        self.printButton.clicked.connect(self.btn_click)
        self.helpButton.clicked.connect(self.btn_click)

        self.setWindowTitle('TopoTable')

        self.show()

    def btn_click(self):                                                                                                                                                                        # Function which runs when a button is pressed
        sender = self.sender()
        if sender.text() == 'Run':                                                                                                                                                              # If run button is pressed...
            try:                                                                                                                                                                                # Try to run the pixelateAndScaleMap backend script
                self.message.setText('')
                pixelateAndScaleMap.fromGUI(folder=self.folderEntry.text(), footprint=self.footprintEntry.text(), n_pillars=self.pixelNumberEntry.text(), s_pillars=self.pixelSizeEntry.text())
                self.message.setText("Completed, files sent to '" + self.folderEntry.text() + "'")                                                                                              # Prints a completed message if successful
            except:
                self.message.setText('Failed, Please Check Conditions And Retry')                                                                                                               # If it fails, print generic error message
        elif sender.text() == 'Browse':                                                                                                                                                         # If browse button is pressed...
            self.folderEntry.setText(QtWidgets.QFileDialog.getExistingDirectory(self, 'Select Directory'))                                                                                      # Opens file browse widget for searching for a directory
        elif sender.text() == 'Help':                                                                                                                                                           # If help button is pressed...
            QtWidgets.QMessageBox.question(self, '', helpDialog, QtWidgets.QMessageBox.Ok)                                                                                                      # Opens help dialog
        elif sender.text() == 'Clear':                                                                                                                                                          # If clear button is pressed...
            self.folderEntry.clear()                                                                                                                                                            # Clears all entry fields
            self.footprintEntry.clear()
            self.pixelNumberEntry.clear()
            self.pixelSizeEntry.clear()
            self.message.setText('')

app = QtWidgets.QApplication(sys.argv)
a_window = Window()
a_window.resize(500,200)
a_window.move(150,200)
sys.exit(app.exec_())