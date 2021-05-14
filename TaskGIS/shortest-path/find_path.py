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
        self.origin_layer = QgsVectorLayer()
        self.destination_layer = QgsVectorLayer()
        self.shortest_path_layers = []
        self.toolPan = tool_file.switchPanTool(self.canvas, self.iface, 'path')
        self.toolZoomIn = tool_file.switchZoomTool(self.canvas, self.iface, False, 'path')
        self.toolZoomOut = tool_file.switchZoomTool(self.canvas, self.iface, True, 'path')
        self.roads_layer = QgsProject.instance().mapLayersByName('Roads')[0]
        self.resetAlteredMaxspeeds()
        QgsMapToolEmitPoint.__init__(self, self.canvas)

    def clearCoords(self):
        try:
            if(self.origin_layer.id()):
                QgsProject.instance().removeMapLayer(self.origin_layer.id())
                self.origin_layer = QgsVectorLayer()

            if(self.destination_layer.id()):
                QgsProject.instance().removeMapLayer(self.destination_layer.id())
                self.destination_layer = QgsVectorLayer()
            
            if(len(self.shortest_path_layers) > 0):
                for shortest_path in self.shortest_path_layers:
                    QgsProject.instance().removeMapLayer(shortest_path.id())
                self.shortest_path_layers = []
        
        except Exception as e:
            self.iface.messageBar().pushMessage("Nothing to clear!", "", level=Qgis.Warning, duration=2)
    
    def resetAlteredMaxspeeds(self):
        with edit(self.roads_layer):
            query = '"maxspeed" = 0'
            selection = self.roads_layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
            for road_feature in selection:
                road_feature['maxspeed'] = 5
                self.roads_layer.updateFeature(road_feature)
                print(road_feature['fid'],':', road_feature['maxspeed'])

    def excludePath(self):
        route_idx = len(self.shortest_path_layers) - 1
        join_params = {
            'DISCARD_NONMATCHING' : False, 
            'INPUT' : self.shortest_path_layers[route_idx],
            'JOIN': self.roads_layer,
            'JOIN_FIELDS' : [],
            'METHOD' : 0,
            'PREDICATE' : [4], 
            'PREFIX' : '',
            'OUTPUT': 'memory:Join'
        }

        join_layer = processing.run("qgis:joinattributesbylocation", join_params)['OUTPUT']
        for join_feature in join_layer.getFeatures():
            with edit(self.roads_layer):
                query = '"fid" = '+str(join_feature['fid'])
                print(join_feature['fid'])
                selection = self.roads_layer.getFeatures(QgsFeatureRequest().setFilterExpression(query))
                for road_feature in selection:
                    road_feature['maxspeed'] = 0
                    self.roads_layer.updateFeature(road_feature)
                    print(road_feature['fid'],':', road_feature['maxspeed'])
            break

    
    def greyPreviousPath(self):
        route_idx = len(self.shortest_path_layers) - 1
        route_layer = self.shortest_path_layers[route_idx]
        route_layer.renderer().symbol().setColor(QColor("#9caaba"))
        route_layer.triggerRepaint()

    def shortestPath(self):
        shortest_path_params = {
            'INPUT':self.roads_layer,
            'START_POINT':'{},{}'.format(self.origin_coords[0], self.origin_coords[1]),
            'END_POINT':'{},{}'.format(self.destination_coords[0], self.destination_coords[1]),
            'STRATEGY':1,
            'ENTRY_COST_CALCULATION_METHOD':0,
            'DIRECTION_FIELD':'SUMMARYDIR',
            'VALUE_BOTH':'',
            'DEFAULT_DIRECTION':2,
            'SPEED_FIELD':'maxspeed',
            'DEFAULT_SPEED':5,
            'TOLERANCE':0,
            'OUTPUT':'memory:Shortest Path '+str(len(self.shortest_path_layers) + 1)
        }

        try:  
            route_layer = processing.run("qneat3:shortestpathpointtopoint", shortest_path_params)['OUTPUT']
            route_layer.renderer().symbol().setColor(QColor("#1372d8"))
            route_layer.renderer().symbol().setWidth(0.86)
            route_layer.triggerRepaint()

            self.shortest_path_layers.append(route_layer)
            QgsProject.instance().addMapLayer(route_layer)
            self.iface.messageBar().pushMessage("(Re) Calculated Shortest Path!", "", level=Qgis.Success, duration=3)
        except Exception as e:
            print(e)
            self.iface.messageBar().pushMessage("No (new) Simple Path found between Orign and Destination!", "", level=Qgis.Warning, duration=3)

    def makePointLayer(self, point_type):
        if(point_type == 'origin'):
            symbol = QgsMarkerSymbol.createSimple({'name': 'triangle', 'color': '#1daa63'})
            symbol.setSize(5)
            origin = QgsVectorLayer("Point", "Origin", "memory")
            origin_features = QgsFeature()
            origin_features.setGeometry(QgsGeometry.fromPointXY(self.origin_coords))
            provider = origin.dataProvider()
            origin.startEditing()
            provider.addFeatures([origin_features])
            origin.commitChanges()

            origin.renderer().setSymbol(symbol)
            self.origin_layer = origin
            QgsProject.instance().addMapLayer(origin)
        else:
            symbol = QgsMarkerSymbol.createSimple({'name': 'triangle', 'color': '#e26b3c'})
            symbol.setSize(5)
            destination = QgsVectorLayer("Point", "Destination", "memory")
            dest_features = QgsFeature()
            dest_features.setGeometry(QgsGeometry.fromPointXY(self.destination_coords))
            provider = destination.dataProvider()
            destination.startEditing()
            provider.addFeatures([dest_features])
            destination.commitChanges()

            destination.renderer().setSymbol(symbol)
            self.destination_layer = destination
            QgsProject.instance().addMapLayer(destination)

    def canvasPressEvent(self, e):
        self.click_count += 1
        if(self.click_count == 1):
            self.origin_coords = self.toMapCoordinates(self.canvas.mouseLastXY())
            self.makePointLayer('origin')
            self.iface.messageBar().pushMessage("Origin coordinates selected!", "Please select Destination coordinates.", level=Qgis.Info, duration=2)
        elif(self.click_count == 2):
            self.destination_coords = self.toMapCoordinates(self.canvas.mouseLastXY())    
            self.makePointLayer('destination')
            self.iface.messageBar().pushMessage("Destination coordinates selected!", "Route calculation will start on pressing Enter...", level=Qgis.Info, duration=2)
        else:
            pass
    
    def keyReleaseEvent(self, e):
        origin_layer = QgsProject.instance().mapLayersByName('Origin')
        destination_layer = QgsProject.instance().mapLayersByName('Destination')

        if(e.key() == 16777220):
            if(len(self.shortest_path_layers) == 0):
                QApplication.instance().setOverrideCursor(Qt.WaitCursor)
                self.shortestPath()
                QApplication.instance().restoreOverrideCursor()
        elif(chr(e.key()) == 'R'):
            if(len(self.shortest_path_layers)>0):
                self.excludePath()
                self.greyPreviousPath()
                QApplication.instance().setOverrideCursor(Qt.WaitCursor)
                self.shortestPath()
                QApplication.instance().restoreOverrideCursor()
        elif(chr(e.key()) == 'Q'):
            self.resetAlteredMaxspeeds()
            self.clearCoords()
            self.canvas.unsetMapTool(self)
        elif(chr(e.key()) == 'P'):
            if(len(origin_layer)==0 and len(destination_layer) == 0):
                self.canvas.setMapTool(self.toolPan)
        elif(chr(e.key()) == 'I'):
            if(len(origin_layer)==0 and len(destination_layer) == 0):
                self.canvas.setMapTool(self.toolZoomIn)
        elif(chr(e.key()) == 'O'):
            if(len(origin_layer)==0 and len(destination_layer) == 0):            
                self.canvas.setMapTool(self.toolZoomOut)




