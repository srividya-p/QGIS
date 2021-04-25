from qgis.gui import * 
from qgis.core import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import Qt 
import sys, os 

class MyWnd(QMainWindow): 
    def __init__(self): 
        QMainWindow.__init__(self) 
        QgsApplication.initQgis() 
        self.canvas = QgsMapCanvas() 
        self.canvas.setCanvasColor(Qt.white) 
        actionZoomIn = QAction("Zoom in", self) 
        actionZoomOut = QAction("Zoom out", self) 
        actionPan = QAction("Pan", self) 
        actionZoomIn.setCheckable(True) 
        actionZoomOut.setCheckable(True) 
        actionPan.setCheckable(True)
        actionZoomIn.triggered.connect(self.zoomIn) 
        actionZoomOut.triggered.connect(self.zoomOut) 
        actionPan.triggered.connect(self.pan) 
        self.toolbar = self.addToolBar("Canvas actions") 
        self.toolbar.addAction (actionZoomIn) 
        self.toolbar.addAction(actionZoomOut) 
        self.toolbar.addAction(actionPan) 
        self.toolPan = QgsMapToolPan(self.canvas) 
        self.toolPan.setAction(actionPan) 
        self.toolZoomIn = QgsMapToolZoom(self.canvas, False) # false = in 
        self.toolZoomIn.setAction(actionZoomIn) 
        self.toolZoomOut = QgsMapToolZoom(self.canvas, True) # true = out 
        self.toolZoomOut.setAction(actionZoomOut)
        self.pan() 
    
    def zoomIn(self): 
            self.canvas.setMapTool(self.toolZoomIn) 
    
    def zoomOut(self): 
        self.canvas.setMapTool(self.toolZoomOut) 
    
    def pan(self): 
        self.canvas.setMapTool(self.toolPan) 
    
class MainApp(QApplication): 
    def __init__(self): 
        QApplication.__init__(self,[],True) 
        wdg = MyWnd() 
        wdg.show() 
        self.exec_()

app = MainApp()