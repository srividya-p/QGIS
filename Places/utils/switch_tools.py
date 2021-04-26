from qgis.core import *
from qgis.gui import *
import importlib.util

approot = QgsProject.instance().homePath()

class switchPanTool(QgsMapToolPan):
    def __init__(self, canvas, iface):
        self.canvas = canvas
        self.iface = iface
        QgsMapToolEmitPoint.__init__(self, self.canvas)
            
    def keyReleaseEvent(self, e):
        circle_spec = importlib.util.spec_from_file_location("draw_circle", approot+"/query-places/draw_circle.py")
        draw_circle_file = importlib.util.module_from_spec(circle_spec)
        circle_spec.loader.exec_module(draw_circle_file)

        draw_tool = draw_circle_file.DrawSectorCircle(self.canvas, self.iface)

        if(chr(e.key()) == 'D'):
            self.canvas.setMapTool(draw_tool)
        elif(chr(e.key()) == 'P'):
            self.canvas.setMapTool(draw_tool.toolPan)
        elif(chr(e.key()) == 'I'):
            self.canvas.setMapTool(draw_tool.toolZoomIn)
        elif(chr(e.key()) == 'O'):
            self.canvas.setMapTool(draw_tool.toolZoomOut)
        elif(chr(e.key()) == 'Q'):
            self.canvas.unsetMapTool(self)

class switchZoomTool(QgsMapToolZoom):
    def __init__(self, canvas, iface, inOut):
        self.canvas = canvas
        self.iface = iface
        QgsMapToolEmitPoint.__init__(self, self.canvas, inOut)
    
    def keyReleaseEvent(self, e):
        circle_spec = importlib.util.spec_from_file_location("draw_circle", approot+"/query-places/draw_circle.py")
        draw_circle_file = importlib.util.module_from_spec(circle_spec)
        circle_spec.loader.exec_module(draw_circle_file)
        
        draw_tool = draw_circle_file.DrawSectorCircle(self.canvas, self.iface)

        if(chr(e.key()) == 'D'):
            self.canvas.setMapTool(draw_tool)
        elif(chr(e.key()) == 'P'):
            self.canvas.setMapTool(draw_tool.toolPan)
        elif(chr(e.key()) == 'I'):
            self.canvas.setMapTool(draw_tool.toolZoomIn)
        elif(chr(e.key()) == 'O'):
            self.canvas.setMapTool(draw_tool.toolZoomOut)
        elif(chr(e.key()) == 'Q'):
            self.canvas.unsetMapTool(self)