import importlib.util
from qgis.core import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import os

approot = QgsProject.instance().homePath()

load_spec = importlib.util.spec_from_file_location("load", approot+"/utils/load.py")
load_file = importlib.util.module_from_spec(load_spec)
load_spec.loader.exec_module(load_file)

circle_spec = importlib.util.spec_from_file_location("draw_circle", approot+"/query-places/draw_circle.py")
draw_circle_file = importlib.util.module_from_spec(circle_spec)
circle_spec.loader.exec_module(draw_circle_file)

path_spec = importlib.util.spec_from_file_location("find_path", approot+"/shortest-path/find_path.py")
find_path_file = importlib.util.module_from_spec(path_spec)
path_spec.loader.exec_module(find_path_file)

intro_text = """<b>Welcome to TaskGIS</b>
<p>TaskGIS lets you to
<ul>
<li><b>Query Sector Places</b> - Find all the Places within a specified radius Sector wise.</li>
<li><b>Find Shortest Path</b> - Find the Shortest Path between the selected origin and destination.</li>
<ul></p>
<p>Shortcuts for tools are present in the Manual section.</p>
<p><i>To Load in Shape files, place them in the folder named 'shape-files' present inside the
Project Root Directory and enter their name CORRECTLY in the 'shape.config.py' file.</i></p>
<p></p>
"""

msgbox = QMessageBox()
msgbox.setWindowTitle('TaskGIS')
msgbox.setStandardButtons(QMessageBox.Close)
msgbox.setText(intro_text)
places_button = msgbox.addButton('Query Places', QMessageBox.AcceptRole)
path_button = msgbox.addButton('Shortest Path', QMessageBox.AcceptRole)
manual_button = msgbox.addButton('Manual', QMessageBox.AcceptRole)

infobox = QMessageBox()
infobox.setWindowTitle('TaskGIS User Manual')
infobox.setStandardButtons(QMessageBox.Close)
info_text = """
The following keys are available as shortcuts:<br>
<p><b>General Shortcuts</b></p>
<p><b>P</b> - Pan over the Canvas</p>
<p><b>I</b> - Zoom into the Canvas</p>
<p><b>O</b> - Zoom out of the Canvas</p>
<p><b>Q</b> - Quit</p> 
<p><b>Query Places Shortcuts</b></p>
<p><b>D</b> - Switch to Draw Circle Tool</p>
<p><b>Shortest Path Shortcuts</b></p>
<p><b>S</b> - Switch to Select Location Tool</p>
<p><b>R</b> - Recalculate Shortest Path</p>
<p>Note - You may switch to Pan or Zoom only before selecting the Origin.</p>
"""
infobox.setText(info_text)

def manual_loop():
    ret = msgbox.exec()
    if ret == QMessageBox.Close:
        QCloseEvent()
    elif msgbox.clickedButton() is places_button:
        success_b = load_file.load_base_layer()
        success_p = load_file.load_places_layer()
        
        if(not success_p):
            iface.messageBar().pushMessage("Error!", "Some of the essential Input Shape File(s) do not exist! Terminating...", level=Qgis.Critical, duration=3)
            QCloseEvent()
            return
        canvas_clicked = draw_circle_file.DrawSectorCircle(iface.mapCanvas(), iface)
        iface.mapCanvas().setMapTool(canvas_clicked)
        iface.messageBar().pushMessage("Welcome", "Select a Center Point.\nPress 'Q' to Quit.", level=Qgis.Info, duration=3)
    elif msgbox.clickedButton() is path_button:
        success_b = load_file.load_base_layer()
        success_p = load_file.load_places_layer()
        success_r = load_file.load_road_layer()

        if(not success_p or not success_r):
            iface.messageBar().pushMessage("Error!", "Some of the essential Input Shape File(s) do not exist! Terminating...", level=Qgis.Critical, duration=3)
            QCloseEvent()
            return
        path_tool = find_path_file.FindPath(iface.mapCanvas(), iface)
        iface.mapCanvas().setMapTool(path_tool)
        iface.messageBar().pushMessage("Welcome", "Select Origin coordinates.\nPress 'Q' to Quit.", level=Qgis.Info, duration=2)
    elif msgbox.clickedButton() is manual_button:
        info_ret = infobox.exec()
    
        if info_ret == QMessageBox.Close:
            QCloseEvent()
            manual_loop()

manual_loop()

