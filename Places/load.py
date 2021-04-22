from qgis.core import *

def load_layers():
    base_layer = QgsVectorLayer(
        '/home/pika/Desktop/QGIS/NE/IND_adm2.shp', "IND_adm2", "ogr")
    places_layer = QgsVectorLayer(
        '/home/pika/Desktop/QGIS/NE/Places.gpkg', "Places", "ogr")

    if(not QgsProject.instance().mapLayersByName('IND_adm2')):
        QgsProject.instance().addMapLayer(base_layer)
        print('Base Layer added to Registry!')
        symbol = QgsFillSymbol.createSimple({'color': 'orange'})
        base_layer.renderer().setSymbol(symbol)
        base_layer.triggerRepaint()

    if(not QgsProject.instance().mapLayersByName('Places')):
        QgsProject.instance().addMapLayer(places_layer)
        print('Places Layer added to Registry!')
        symbol = QgsMarkerSymbol.createSimple(
            {'name': 'circle', 'color': 'green'})
        places_layer.renderer().setSymbol(symbol)
        places_layer.triggerRepaint()

