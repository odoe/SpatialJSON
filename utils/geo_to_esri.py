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

  # This will hold the geojson geometry type
  geo_type = ""
  # check for collection of features
  # and iterate as necessary
  attribute_fields = []
  if geojson["type"] == "FeatureCollection":
    features = geojson["features"]
    geo_type = features[0]["geometry"]["type"]
    attribute_fields = features[0]["properties"]

    esri_features = map(extract, features)
  else:
    attribute_fields = geojson["properties"]
    geo_type = geojson["geometry"]["type"]
    esri_features = extract(geojson)

  fields = map(extract_field, attribute_fields)
  # everything should be ready to define for the
  # esri json
  esri["geometryType"] = get_geom_type(geo_type)
  esri["spatialReference"] = sr
  esri["fields"] = fields
  esri["features"] = esri_features

  return esri

def extract(feature):
  # parse out the geometry data
  geometry = get_geometry(feature)
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

def get_geom_type(geo_type):
  if geo_type == "Point":
    return "esriGeometryPoint"
  elif geo_type == "MultiPoint":
    return "esriGeometryMultiPoint"
  elif geo_type == "LineString":
    return "esriGeometryPolyline"
  elif geo_type == "Polygon":
    return "esriGeometryPolygon"
  else:
    return "unknown"

def get_geometry(feature):
  # match how geometry is represented
  # based on the geojson geometry type
  geometry = {}
  geom = feature["geometry"]
  geo_type = geom["type"]
  if geo_type == "Point":
    geometry["x"] = geom["coordinates"][0]
    geometry["y"] = geom["coordinates"][1]
  elif geo_type == "Polygon":
    geometry["rings"] = geom
  elif geo_type =="LineString":
    geometry["paths"] = geom

  return geometry
