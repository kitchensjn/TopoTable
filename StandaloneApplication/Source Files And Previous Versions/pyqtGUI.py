"""
PyQt Graphical User Interface

James Kitchens - 08/31/2019

Frontend of the map conversion. This code communicates with the backend program used to take maps downloaded from 'terrain.party'
and produce a .csv file with associated heights of each pillar to display map to scale. Running this code opens a new window with
inputs used to set parameters for backend.
"""

import sys, os
import pixelateAndScaleMap
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QSizePolicy, QPushButton, QLabel, QLineEdit
from PyQt5.QtGui import QPixmap

import matplotlib
matplotlib.use('PS')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D


helpDialog = """Help Dialog\n
Folder: the path to the directory which contains the desired maps and README.txt\n
Footprint: taken from terrain.party, the size of one dimension of the square in meters (8km x 8km = 8000). Leave off units!\n
PillarNumber: the number of pillars which make up one dimension of the table (100pillars x 100pillars = 100)\n
PillarSize: the size of one dimension of an individual pillar (length or width), generally 1. Leave off units!\n
"""                                                                                                                                                                                             # Help dialog text explaining each entry dialog


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class Window(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.left = 0
        self.top = 10
        self.width = 780
        self.height = 450
        self.init_ui()

    def init_ui(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setFixedSize(self.width, self.height)

        self.folderLabel = QLabel('Folder', self)                                                                                                                                           # Sets up the labels for each entry dialog
        self.folderLabel.setFont(QtGui.QFont('Times', 15))
        self.folderEntry = QLineEdit(self)
        self.browseButton = QPushButton('Browse', self)

        self.footprintLabel = QLabel('Footprint', self)
        self.footprintLabel.setFont(QtGui.QFont('Times', 15))
        self.footprintEntry = QLineEdit(self)
        self.footprintEntry.setFixedWidth(300)

        self.pixelNumberLabel = QLabel('PillarNumber', self)
        self.pixelNumberLabel.setFont(QtGui.QFont('Times', 15))
        self.pixelNumberEntry = QLineEdit(self)

        self.pixelSizeLabel = QLabel('PillarSize', self)
        self.pixelSizeLabel.setFont(QtGui.QFont('Times', 15))
        self.pixelSizeEntry = QLineEdit(self)

        self.message = QLabel('', self)
        self.message.setFont(QtGui.QFont('Times', 10))

        self.clearButton = QPushButton('Clear', self)
        self.printButton = QPushButton('Run', self)

        self.helpButton = QPushButton('Help', self)

        self.plotTitle = QLabel('Visualization of Your Map', self)
        self.plotTitle.setFont(QtGui.QFont('Times', 20, QtGui.QFont.Bold))
        self.plotDescription = QLabel('Available only for maps smaller than 30 pillars by 30 pillars', self)
        self.plotDescription.setFont(QtGui.QFont('Times', 15))
        self.mapPlot = PlotCanvas(self, width=8, height=5)

        self.logo = QLabel(self)
        pixmap = QPixmap(resource_path('TopoTableLogoSmaller.png'))
        self.logo.setPixmap(pixmap)
        self.resize(pixmap.width(), pixmap.height())
        self.bigTitle = QLabel('TopoTable', self)
        self.bigTitle.setFont(QtGui.QFont('Times', 40, QtGui.QFont.Bold))
        self.bigDescription = QLabel('A dynamic raised relief map table by James Kitchens', self)
        self.bigDescription.setFont(QtGui.QFont('Times', 20))

        h_box0 = QtWidgets.QHBoxLayout()  # Creates folder entry dialog
        h_box0.addWidget(self.folderLabel)
        h_box0.addWidget(self.folderEntry)
        h_box0.addWidget(self.browseButton)

        h_box1 = QtWidgets.QHBoxLayout()  # Creates footprint entry dialog
        h_box1.addWidget(self.footprintLabel)
        h_box1.addWidget(self.footprintEntry)

        h_box2 = QtWidgets.QHBoxLayout()
        h_box2.addWidget(self.pixelNumberLabel)
        h_box2.addWidget(self.pixelNumberEntry)

        h_box3 = QtWidgets.QHBoxLayout()
        h_box3.addWidget(self.pixelSizeLabel)
        h_box3.addWidget(self.pixelSizeEntry)

        h_box4 = QtWidgets.QHBoxLayout()
        h_box4.addStretch()
        h_box4.addWidget(self.message)
        h_box4.addStretch()

        h_box5 = QtWidgets.QHBoxLayout()
        h_box5.addStretch()
        h_box5.addWidget(self.clearButton)
        h_box5.addStretch()
        h_box5.addWidget(self.printButton)
        h_box5.addStretch()

        h_box6 = QtWidgets.QHBoxLayout()
        h_box6.addWidget(self.helpButton)
        h_box6.addStretch()

        v_box1 = QtWidgets.QVBoxLayout()  # Sets layout and order of dialogs
        #v_box1.addStretch()
        v_box1.addLayout(h_box0)
        v_box1.addLayout(h_box1)
        v_box1.addLayout(h_box2)
        v_box1.addLayout(h_box3)
        v_box1.addLayout(h_box5)
        #v_box1.addStretch()
        v_box1.addLayout(h_box4)
        #v_box1.addStretch()
        v_box1.addLayout(h_box6)
        #v_box1.addStretch()

        h_box7 = QtWidgets.QHBoxLayout()
        h_box7.addStretch()
        h_box7.addWidget(self.plotTitle)
        h_box7.addStretch()

        h_box8 = QtWidgets.QHBoxLayout()
        h_box8.addStretch()
        h_box8.addWidget(self.plotDescription)
        h_box8.addStretch()

        h_box9 = QtWidgets.QHBoxLayout()
        h_box9.addWidget(self.mapPlot)

        v_box2 = QtWidgets.QVBoxLayout()  # Sets layout and order of dialogs
        v_box2.addStretch()
        v_box2.addLayout(h_box7)
        v_box2.addStretch()
        v_box2.addLayout(h_box8)
        v_box2.addStretch()
        v_box2.addLayout(h_box9)
        v_box2.addStretch()

        h_box10 = QtWidgets.QHBoxLayout()
        h_box10.addLayout(v_box1)
        h_box10.addLayout(v_box2)

        h_box11 = QtWidgets.QHBoxLayout()
        h_box11.addStretch()
        h_box11.addWidget(self.logo)
        h_box11.addStretch()
        h_box11.addWidget(self.bigTitle)
        h_box11.addWidget(self.bigDescription)
        h_box11.addStretch()

        v_box4 = QtWidgets.QVBoxLayout()
        v_box4.addStretch()
        v_box4.addLayout(h_box11)
        v_box4.addStretch()
        v_box4.addLayout(h_box10)
        v_box4.addStretch()
        self.setLayout(v_box4)
        self.browseButton.clicked.connect(self.btn_click)
        self.clearButton.clicked.connect(self.btn_click)
        self.printButton.clicked.connect(self.btn_click)
        self.helpButton.clicked.connect(self.btn_click)
        self.setWindowTitle('TopoTable for OSX')
        self.show()

    def btn_click(self):                                                                                                                                                                        # Function which runs when a button is pressed
        sender = self.sender()
        if sender.text() == 'Run':                                                                                                                                                              # If run button is pressed...
            self.mapPlot.axes.figure.clear()
            self.mapPlot.axes.figure.canvas.draw_idle()
            try:                                                                                                                                                                                # Try to run the pixelateAndScaleMap backend script
                self.message.setText('')
                outFileName = pixelateAndScaleMap.fromGUI(folder=self.folderEntry.text(), footprint=self.footprintEntry.text(), n_pillars=self.pixelNumberEntry.text(), s_pillars=self.pixelSizeEntry.text())
                self.message.setText("Completed, files sent to 'Folder' directory")
                #self.message.setText("Completed, files sent to '" + self.folderEntry.text() + "'")                                                                                              # Prints a completed message if successful
                if int(self.pixelNumberEntry.text()) <= 30:
                    self.mapPlot.plot(mapCSVpath=outFileName, pillarNumber=self.pixelNumberEntry.text(), pillarSize=self.pixelSizeEntry.text())
            except:
                self.message.setText('Failed, Please Check Conditions And Retry')                                                                                                                 # If it fails, print generic error message
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
            self.mapPlot.axes.figure.clear()
            self.mapPlot.axes.figure.canvas.draw_idle()


class PlotCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100, J=0):
        fig = Figure(figsize=(width, height), dpi=dpi)
        fig.set_facecolor('white')
        self.axes = fig.add_subplot(111)

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
        self.axes.figure.clear()
        self.axes.figure.canvas.draw_idle()

    def plot(self, mapCSVpath, pillarNumber, pillarSize):
        mapData = open(mapCSVpath, 'r')
        x = []
        y = []
        z = []
        b = []
        maxRange = float(pillarNumber)
        for line in mapData:
            line = line.replace('\n', '').split(',')
            y.append(int(line[0])*float(pillarSize))
            x.append(int(line[1])*float(pillarSize))
            if float(line[2]) > maxRange:
                maxRange = float(line[2])
            z.append(float(line[2]))
            b.append(0)
        ax = self.figure.add_subplot(111, projection='3d')
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
        ax.axis('off')
        ax.set_xlim3d(0, maxRange)
        ax.set_ylim3d(0, maxRange)
        ax.set_zlim3d(0, maxRange)
        ax.bar3d(x, y, b, float(pillarSize), float(pillarSize), z, 'white', edgecolor='black')
        self.draw()


app = QtWidgets.QApplication(sys.argv)
a_window = Window()
sys.exit(app.exec_())