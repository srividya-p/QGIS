layer = iface.activeLayer()

features = layer.getFeatures()

places_data = []
for f in features:
    place = dict()
    
    place['name'] = f['name']
    place['fid'] = f['fid']
    place['fclass'] = f['fclass']
    place['population'] = f['population']
    place['osm_id'] = f['osm_id']
    place['code'] = f['code']
    
    places_data.append(place)