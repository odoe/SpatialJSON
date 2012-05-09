"""
This script will convert an EsriJSON
dictionary to a GeoJSON dictionary

send a GeoJSON feature:
feature = json.loads(esri_input)
result = esri_to_geo(feature)
optional: response = json.dumps(result)

Still in the works:
- parse all geometry types
"""
def esri_to_geo(esrijson):
  geojson = {}
  geojson["type"] = "Feature"
  # first, grab the properties
  features = esrijson["features"]
  properties = features["attributes"]
  # we're going to assume we are
  # only using points for now
  geom = features["geometry"]
  geometry = {}
  geometry["type"] = "Point"
  geometry["coordinates"] = [ geom["x"], geom["y"] ]
  geojson["geometry"] = geometry
  geojson["properties"] = properties
  
  return geojson
