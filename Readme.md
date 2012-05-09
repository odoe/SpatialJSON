# Spatial JSON Converter #

This is an API Rest service built using Python Bottle to convert between ESRI JSON and GeoJSON.
This is a bare minimum REST API at the moment that will only work
properly with points. I started this project in response to a [code
challenge](http://fredboyle.com/codechallenge/) to try something new.

I am currently expanding use of this API in [this project](https://github.com/odoe/Geo-Like) using MongoDB to store the GeoJSON data.

TODO:

* Add error checking in conversions (goejson sent to geojson to esrijson, etc)
* Add handlers for more geometry types
