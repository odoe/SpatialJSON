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

  # handle the geometry
  # for now, simple points
  # for now, let's stick with simple points
  esri["geometryType"] = "esriGeometryPoint"
  esri["spatialReference"] = sr

  # check for collection of features
  # and iterate as necessary
  attribute_fields = []
  if geojson["type"] == "FeatureCollection":
    features = geojson["features"]
    attribute_fields = features[0]["properties"]

    esri_features = map(extract, features)
  else:
    attribute_fields = geojson["properties"]
    esri_features = extract(geojson)

  fields = map(extract_field, attribute_fields)
  esri["fields"] = fields
  esri["features"] = esri_features

  return esri

def extract(feature):
  geometry = {}
  # drill down and grab the geometry data
  geometry["x"] = feature["geometry"]["coordinates"][0]
  geometry["y"] = feature["geometry"]["coordinates"][1]
  out_feature = {}
  out_feature["geometry"] = geometry
  out_feature["attributes"] = feature["properties"]

  return out_feature

def extract_field(attribute):
  # now we need the fields in the properties
  a = {}
  a["alias"] = attribute
  a["name"] = attribute
  if isinstance(attribute, int):
    a["type"] = "esriFieldTypeSmallInteger"
  elif isinstance(attribute, float):
    a["type"] = "esriFieldTypeDouble"
  else:
    a["type"] = "esriFieldTypeString"
    a["length"] = 70
  return a
