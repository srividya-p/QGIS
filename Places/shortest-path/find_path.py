from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import importlib.util

import processing

approot = QgsProject.instance().homePath()

tool_spec = importlib.util.spec_from_file_location("tool", approot+"/utils/switch_tools.py")
tool_file = importlib.util.module_from_spec(tool_spec)
tool_spec.loader.exec_module(tool_file)

class FindPath(QgsMapTool):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        self.click_count = 0
        self.origin_coords = QgsPointXY()
        self.destination_coords = QgsPointXY()
        self.toolPan = tool_file.switchPanTool(self.canvas, self.iface)
        self.toolZoomIn = tool_file.switchZoomTool(self.canvas, self.iface, False)
        self.toolZoomOut = tool_file.switchZoomTool(self.canvas, self.iface, True)
        QgsMapToolEmitPoint.__init__(self, self.canvas)

    def shortest_path(self):
        roads_layer = QgsProject.instance().mapLayersByName('Roads')[0]
        params = {
            'INPUT':roads_layer,
            'START_POINT':'{},{}'.format(self.origin_coords[0], self.origin_coords[1]),
            'END_POINT':'{},{}'.format(self.destination_coords[0], self.destination_coords[1]),
            'STRATEGY':0,
            'ENTRY_COST_CALCULATION_METHOD':0,
            'DIRECTION_FIELD':'SUMMARYDIR',
            'VALUE_BOTH':'',
            'DEFAULT_DIRECTION':2,
            'SPEED_FIELD':None,
            'DEFAULT_SPEED':5,
            'TOLERANCE':0,
            'OUTPUT':'memory:Shortest Path'
        }
            
        route_layer = processing.run("qneat3:shortestpathpointtopoint", params)['OUTPUT']
        route_layer.renderer().symbol().setColor(QColor("#17137c"))
        route_layer.renderer().symbol().setWidth(0.86)
        route_layer.triggerRepaint()

        QgsProject.instance().addMapLayer(route_layer)

    def make_point_layer(self, point_type):
        symbol = QgsMarkerSymbol.createSimple({'name': 'triangle', 'color': 'red'})
        symbol.setSize(5)

        if(point_type == 'origin'):
            origin = QgsVectorLayer("Point", "Origin", "memory")
            origin_features = QgsFeature()
            origin_features.setGeometry(QgsGeometry.fromPointXY(self.origin_coords))
            provider = origin.dataProvider()
            origin.startEditing()
            provider.addFeatures([origin_features])
            origin.commitChanges()

            origin.renderer().setSymbol(symbol)
            QgsProject.instance().addMapLayer(origin)
        else:
            destination = QgsVectorLayer("Point", "Destination", "memory")
            dest_features = QgsFeature()
            dest_features.setGeometry(QgsGeometry.fromPointXY(self.destination_coords))
            provider = destination.dataProvider()
            destination.startEditing()
            provider.addFeatures([dest_features])
            destination.commitChanges()

            destination.renderer().setSymbol(symbol)
            QgsProject.instance().addMapLayer(destination)


    def canvasPressEvent(self, e):
        self.click_count += 1
        if(self.click_count == 1):
            self.origin_coords = self.toMapCoordinates(self.canvas.mouseLastXY())
            self.make_point_layer('origin')
            self.iface.messageBar().pushMessage("Origin coordinates selected!", "Please select Destination coordinates.", level=Qgis.Info, duration=2)
        elif(self.click_count == 2):
            self.destination_coords = self.toMapCoordinates(self.canvas.mouseLastXY())    
            self.make_point_layer('destination')
            self.iface.messageBar().pushMessage("Destination coordinates selected!", "Route calculation will start on pressing Enter...", level=Qgis.Info, duration=2)
        else:
            pass
    
    def keyReleaseEvent(self, e):
        if(e.key() == 16777220):
            QApplication.instance().setOverrideCursor(Qt.WaitCursor)
            self.shortest_path()
            QApplication.instance().restoreOverrideCursor()
            self.iface.messageBar().pushMessage("Calculated Shortest Path!", "", level=Qgis.Success, duration=3)
            self.click_count = 0
        elif(chr(e.key()) == 'Q'):
            self.canvas.unsetMapTool(self)
        elif(chr(e.key()) == 'P'):
            self.canvas.setMapTool(self.toolPan)
        elif(chr(e.key()) == 'I'):
            self.canvas.setMapTool(self.toolZoomIn)
        elif(chr(e.key()) == 'O'):
            self.canvas.setMapTool(self.toolZoomOut)


