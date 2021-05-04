canvas = QgsMapCanvas()
canvas.show()    

canvas.setCanvasColor(Qt.white)
canvas.enableAntiAliasing(True)

base_layer = QgsVectorLayer('/home/pika/Desktop/QGIS/NE/IND_adm2.shp', "IND_adm2", "ogr")
places_layer = QgsVectorLayer('/home/pika/Desktop/QGIS/NE/Places.gpkg', "Places", "ogr")

canvas_layers = [places_layer, base_layer]

if(not QgsProject.instance().mapLayersByName('IND_adm2')):
    QgsProject.instance().addMapLayer(base_layer)
    print('Base Layer added to Registry!')

if(not QgsProject.instance().mapLayersByName('Places')):
    QgsProject.instance().addMapLayer(places_layer)
    print('Places Layer added to Registry!')

canvas.setExtent(base_layer.extent())
canvas.setLayers(canvas_layers)
canvas.zoomIn()