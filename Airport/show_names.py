op_file = open('/home/pika/Desktop/QGIS/Airport/airports.txt', 'w')

layer = iface.activeLayer()

#print(dir(layer))

#print(layer.getFeatures())

features = layer.getFeatures()

for f in features:
    #print(f['name'], f['iata_code'])
    geom = f.geometry()
    #geom.asPoint()
    line = str(f['name'])+', '+str( f['iata_code']) +', '+str(geom.asPoint ().x())+', '+ str(geom.asPoint ().y())+'\n'
    unicode_line = line.encode ('utf-8')
    op_file.write(line)

print('File with Airport details created!')

op_file.close()
    

