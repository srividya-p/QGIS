import importlib.util
from qgis.core import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

approot = QgsProject.instance().homePath()

load_spec = importlib.util.spec_from_file_location("load", approot+"/load.py")
load_file = importlib.util.module_from_spec(load_spec)
load_spec.loader.exec_module(load_file)

circle_spec = importlib.util.spec_from_file_location("draw_circle", approot+"/draw_circle.py")
draw_circle_file = importlib.util.module_from_spec(circle_spec)
circle_spec.loader.exec_module(draw_circle_file)

msgbox = QMessageBox()
msgbox.setWindowTitle('Welcome to TaskGIS')
msgbox.setStandardButtons(QMessageBox.Close)
msgbox.setText(' Choose the Task to be performed')
places_button = msgbox.addButton('Query Places', QMessageBox.AcceptRole)
path_button = msgbox.addButton('Shortest Path', QMessageBox.AcceptRole)

ret = msgbox.exec()

if ret == QMessageBox.Close:
    QCloseEvent()
elif msgbox.clickedButton() is places_button:
    load_file.load_places_layers()
    canvas_clicked = draw_circle_file.DrawSectorCircle(iface.mapCanvas(), iface)
    iface.mapCanvas().setMapTool(canvas_clicked)
    iface.messageBar().pushMessage("Welcome", "Select a Center Point.\nPress 'Q' to Quit.", level=Qgis.Info, duration=3)
elif msgbox.clickedButton() is path_button:
    load_file.load_path_layers()