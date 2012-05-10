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
  if geojson["type"] == "FeatureCollection":
    features = geojson["features"]
    attribute_fields = features[0]["properties"]
    esri_features = []
    for feat in features:
      item = extract(feat)
      esri_features.append(item)

    fields = extract_fields(attribute_fields)
    esri["fields"] = fields
    esri["features"] = esri_features
  else:
    attribute_fields = geojson["properties"]
    fields = extract_fields(attribute_fields)
    esri_feature = extract(geojson)
    esri["fields"] = fields
    esri["features"] = esri_feature

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

def extract_fields(attributes):
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

  return fields
