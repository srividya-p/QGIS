import importlib.util
import os

load_spec = importlib.util.spec_from_file_location("load", "/home/pika/Desktop/QGIS/Python/Places/load.py")
load_file = importlib.util.module_from_spec(load_spec)
load_spec.loader.exec_module(load_file)

circle_spec = importlib.util.spec_from_file_location("draw_circle", "/home/pika/Desktop/QGIS/Python/Places/draw_circle.py")
draw_circle_file = importlib.util.module_from_spec(circle_spec)
circle_spec.loader.exec_module(draw_circle_file)

print(os.getcwd())

load_file.load_layers()
canvas_clicked = draw_circle_file.DrawSectorCircle(iface.mapCanvas(), iface)
iface.mapCanvas().setMapTool(canvas_clicked)
iface.messageBar().pushMessage("Welcome",
                               "Select a Center Point.\nPress 'Q' to Quit.", level=Qgis.Info, duration=3)
