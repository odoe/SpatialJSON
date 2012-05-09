"""
This script will convert a GeoJSON
dictionary to an EsriJSON dictionary

send a GeoJSON feature:
feature = json.loads(json_input)
result = geo_to_esri(feature)
optional: response = json.dumps(result)

Still in the works:
- parse all geometry types
- possible handle a collection of features
"""
def geo_to_esri(geojson):
	esri = {}
	
	# we already know the spatial reference we want
	# for geojson, at least in this simple case
	sr = {"wkid": 4326}

	# grab the geojson properties first
	attributes = geojson["properties"]
	# now we need the fields in the properties
	fields = []
	for f in attributes:
		a = {}
		a["alias"] = f
		a["name"] = f
		if isinstance(f, int):
			a["type"] = "esriFieldTypeSmallInteger"
		elif isinstance(f, float):
			a["type"] = "esriFieldTypeDouble"
		else:
			a["type"] = "esriFieldTypeString"
			a["length"] = 70
		fields.append(a)
	
	esri["fields"] = fields
	
	# handle the geometry
	# for now, simple points
	# for now, let's stick with simple points
	esri["geometryType"] = "esriGeometryPoint"
	geometry = {}
	geometry["x"] = geojson["geometry"]["coordinates"][0]
	geometry["y"] = geojson["geometry"]["coordinates"][1]
	features = {}
	features["geometry"] = geometry
	features["attributes"] = attributes
	esri["features"] = features
	
	return esri
	
	
