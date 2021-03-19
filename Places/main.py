import os
print(os.getcwd())

load_layers()
canvas_clicked = DrawSectorCircle(iface.mapCanvas(), iface)
iface.mapCanvas().setMapTool(canvas_clicked)
iface.messageBar().pushMessage("Welcome",
                               "Select a Center Point.\nPress 'Q' to Quit.", level=Qgis.Info, duration=0)
