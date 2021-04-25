from qgis.core import *

def load_layers():
    base_layer = QgsVectorLayer(
        '/home/pika/Desktop/QGIS/Shape-Files/Base-Map/IND_adm2.shp', "Base Map", "ogr")
    places_layer = QgsVectorLayer(
        '/home/pika/Desktop/QGIS/Shape-Files/Places/Places.gpkg', "Places", "ogr")

    if(not QgsProject.instance().mapLayersByName('Base Map')):
        QgsProject.instance().addMapLayer(base_layer)
        print('Base Layer added to Registry!')
        symbol = QgsFillSymbol.createSimple({'color': '#e6cff2'})
        base_layer.renderer().setSymbol(symbol)
        base_layer.triggerRepaint()

    if(not QgsProject.instance().mapLayersByName('Places')):
        QgsProject.instance().addMapLayer(places_layer)
        print('Places Layer added to Registry!')
        symbol = QgsMarkerSymbol.createSimple(
            {'name': 'circle', 'color': 'green'})
        places_layer.renderer().setSymbol(symbol)
        places_layer.triggerRepaint()

