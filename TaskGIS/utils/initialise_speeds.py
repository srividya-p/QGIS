from qgis.core import *
from PyQt5.QtGui import *

roads_layer = QgsProject.instance().mapLayersByName('Roads')[0]

print('Initialising speeds...')
i=0
with edit(roads_layer):
    for feature in roads_layer.getFeatures():
        print('Feature =',i)
        feature['maxspeed'] = 5
        roads_layer.updateFeature(feature)
        i+=1

print('Initialised Speeds successfully!')
