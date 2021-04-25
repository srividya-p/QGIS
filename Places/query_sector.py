from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

import importlib.util
import processing
import math
pi = math.pi

class QuerySectorPlaces(QgsMapTool):
    def __init__(self, canvas, iface, point, radius, line_layers, circle):
        self.canvas = canvas
        self.iface = iface
        self.center_x = point[0]
        self.center_y = point[1]
        self.x = 0
        self.y = 0
        self.radius = radius
        self.sector_layer = QgsVectorLayer()
        self.circle = circle
        self.line_layers = line_layers
        QgsMapToolEmitPoint.__init__(self, self.canvas)

    def clearCanvas(self):
        if(len(self.line_layers) > 0):
            for line in self.line_layers:
                QgsProject.instance().removeMapLayer(line.id())

            QgsProject.instance().removeMapLayer(self.circle.id())

            self.line_layers = []
            self.circle = QgsVectorLayer()

    def clearSector(self):
        if(self.sector_layer.id()):
            QgsProject.instance().removeMapLayer(self.sector_layer.id())
            self.sector_layer = QgsVectorLayer()

    def drawSector(self, n, r):
        arc_start = [self.center_x+(r*math.cos((2*n*pi)/16)),
                     self.center_y+(r*math.sin((2*n*pi)/16))]
        arc_end = [self.center_x+(r*math.cos((2*(n+1)*pi)/16)),
                   self.center_y+(r*math.sin((2*(n+1)*pi)/16))]
        arc_mid = [self.center_x+(r*math.cos((2*n*pi + 2*(n+1)*pi)/32)),
                   self.center_y+(r*math.sin((2*n*pi + 2*(n+1)*pi)/32))]

        arc = QgsVectorLayer(
            "LineString?crs=epsg:4326&field=id:integer&field=name:string(20)&index=yes", "line", "memory")
        arc_geom = QgsCircularString()
        arc_geom.setPoints([
            QgsPoint(arc_start[0], arc_start[1]),
            QgsPoint(arc_mid[0], arc_mid[1]),
            QgsPoint(arc_end[0], arc_end[1])]
        )
        arc_feature = QgsFeature()
        arc_feature.setGeometry(QgsGeometry(arc_geom))

        line1_start = QgsPointXY(self.center_x, self.center_y)
        line1_mid = QgsPointXY(
            (self.center_x+arc_start[0])/2, (self.center_y+arc_start[1])/2)
        line1_end = QgsPointXY(arc_start[0], arc_start[1])
        line1 = QgsVectorLayer("LineString", "line", "memory")
        seg1 = QgsFeature()
        seg1.setGeometry(QgsGeometry.fromPolylineXY(
            [line1_start, line1_mid, line1_end]))

        line2_start = QgsPointXY(self.center_x, self.center_y)
        line2_mid = QgsPointXY(
            (self.center_x+arc_end[0])/2, (self.center_y+arc_end[1])/2)
        line2_end = QgsPointXY(arc_end[0], arc_end[1])
        line2 = QgsVectorLayer("LineString", "line", "memory")
        seg2 = QgsFeature()
        seg2.setGeometry(QgsGeometry.fromPolylineXY(
            [line2_start, line2_mid, line2_end]))

        merged = QgsVectorLayer("LineString", "Sector "+str(n+1), "memory")
        provider = merged.dataProvider()

        merged.startEditing()
        provider.addFeatures([seg1])
        provider.addFeatures([seg2])
        provider.addFeatures([arc_feature])
        merged.commitChanges()

        sector = processing.run("qgis:polygonize", {
                                'INPUT': merged, 'OUTPUT': 'memory:Sector '+str(n+1)})["OUTPUT"]

        QgsProject.instance().addMapLayer(sector)
        symbol = QgsFillSymbol.createSimple(
            {'style': 'no', 'outline_style': 'solid', 'outline_width': '0.5', 'outline_color': 'blue'})
        sector.renderer().setSymbol(symbol)
        sector.triggerRepaint()

        self.sector_layer = sector

    def identifySector(self):
        dy = self.y - self.center_y
        dx = self.x - self.center_x
        angle = math.atan2(dy, dx)

        if angle < 0:
            angle = angle+2*pi

        sector_num = int(angle//((2*pi)/16))
        self.drawSector(sector_num, self.radius)
        return sector_num+1

    def getNamesInPolygon(self, n):
        pointLayer = QgsProject.instance().mapLayersByName('Places')[0]
        places_in_sector = ''
        for a in self.sector_layer.getFeatures():
            for b in pointLayer.getFeatures():
                if a.geometry().contains(b.geometry()):
                    places_in_sector += str(b['name'])+'\n'

        QMessageBox().information(None, "Places - Sector "+str(n), places_in_sector)

    def canvasPressEvent(self, e):
        self.clearSector()

        point = self.toMapCoordinates(self.canvas.mouseLastXY())
        self.x = point[0]
        self.y = point[1]
        print ('Sector - ({:.4f}, {:.4f})'.format(self.x, self.y))

        n = self.identifySector()
        self.getNamesInPolygon(n)

    def keyReleaseEvent(self, e):
        if(chr(e.key()) == 'Q'):
            self.clearSector()
            self.clearCanvas()
            self.canvas.unsetMapTool(self)
        elif(chr(e.key()) == 'L'):
            self.clearSector()
            self.clearCanvas()

            circle_spec = importlib.util.spec_from_file_location("draw_circle", "/home/pika/Desktop/QGIS/Places/draw_circle.py")
            draw_circle_file = importlib.util.module_from_spec(circle_spec)
            circle_spec.loader.exec_module(draw_circle_file)

            canvas_clicked = draw_circle_file.DrawSectorCircle(self.iface.mapCanvas(), self.iface)
            self.iface.mapCanvas().setMapTool(canvas_clicked)

