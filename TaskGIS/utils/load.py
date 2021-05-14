from qgis.core import *
from PyQt5.QtGui import *
import importlib.util
from os import path

approot = QgsProject.instance().homePath()

path_spec = importlib.util.spec_from_file_location("shape", approot+"/shape.config.py")
path_file = importlib.util.module_from_spec(path_spec)
path_spec.loader.exec_module(path_file)

base_path = approot+'/shape-files/'+path_file.BASE_MAP
places_path = approot+'/shape-files/'+path_file.PLACES
roads_path = approot+'/shape-files/'+path_file.ROADS

def load_base_layer():
    if(path.exists(base_path)):
        base_layer = QgsVectorLayer(base_path, "Base Map", "ogr")
        if(not QgsProject.instance().mapLayersByName('Base Map')):
            if(QgsProject.instance().mapLayersByName('Places')):
                places=QgsProject.instance().mapLayersByName('Places')[0]
                QgsProject.instance().removeMapLayers([places.id()])
            if(QgsProject.instance().mapLayersByName('Roads')):
                roads=QgsProject.instance().mapLayersByName('Roads')[0]
                QgsProject.instance().removeMapLayers([roads.id()])
            QgsProject.instance().addMapLayer(base_layer)
            print('Base Layer added to Registry!')
            symbol = QgsFillSymbol.createSimple({'color': '#e6cff2'})
            base_layer.renderer().setSymbol(symbol)
            base_layer.triggerRepaint()
    else:
        return False

    return True

def load_places_layer():
    if(path.exists(places_path)):
        places_layer = QgsVectorLayer(places_path, "Places", "ogr")
        if(not QgsProject.instance().mapLayersByName('Places')):
            QgsProject.instance().addMapLayer(places_layer)
            print('Places Layer added to Registry!')
            symbol = QgsMarkerSymbol.createSimple(
                {'name': 'circle', 'color': 'green'})
            places_layer.renderer().setSymbol(symbol)
            places_layer.triggerRepaint()
    else:
        return False
    
    return True

def load_road_layer():    
    if(path.exists(roads_path)):
        roads_layer = QgsVectorLayer(roads_path, "Roads", "ogr")
        if(not QgsProject.instance().mapLayersByName('Roads')):
            roads_layer.renderer().symbol().setColor(QColor("brown"))
            roads_layer.triggerRepaint()
            QgsProject.instance().addMapLayer(roads_layer)
            print('Roads Layer added to Registry!')
    else:
        return False
    
    return True


