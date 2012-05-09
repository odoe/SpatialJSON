import json
import bottle
from utils.geo_to_esri import geo_to_esri
from utils.esri_to_geo import esri_to_geo
from bottle import route, run, request, abort

# This path will take a GeoJSON
# and convert it to EsriJSON to save
@route('/togeojs', method='PUT')
def put_geojs():
  data = request.body.readline()
  if not data:
    abort(400, 'No data received')
  entity = json.loads(data)

  result = esri_to_geo(entity)

  return result

# This path will take an EsriJSON
# and convert it to GeoJSON to save
@route('/toesrijs', method='PUT')
def put_esrijs():
  data = request.body.readline()
  if not data:
    abort(400, 'No data received')
  entity = json.loads(data)

  result = geo_to_esri(entity)

  return result

run(host='localhost', port=8080)
