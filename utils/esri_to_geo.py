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
  # first, grab the properties
  features = esrijson["features"]

  count = len(features)

  if count > 1:
    geojson["type"] = "FeatureCollection"
  else:
    geojson["type"] = "Feature"

  feats = []
  for feature in features:
    feat = extract(feature)
    feats.append(feat)
  geojson["features"] = feats

  return geojson

def extract(feature):
  item = {}
  item["type"] = "Feature"
  # can just make a direct
  # copy of the attributes to properties
  properties = feature["attributes"]
  # we're going to assume we are
  # only using points for now
  geom = feature["geometry"]
  geometry = {}
  geometry["type"] = "Point"
  geometry["coordinates"] = [ geom["x"], geom["y"] ]
  item["geometry"] = geometry
  item["properties"] = properties

  return item
