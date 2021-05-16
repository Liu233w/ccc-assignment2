const GeoJsonGeometriesLookup = require('geojson-geometries-lookup')
const geojson = require('./polygons.json')
const glookup = new GeoJsonGeometriesLookup(geojson)

module.exports = function (map) {
  const bbox = map.geo.place.geo.bbox
  const container = glookup.getContainers({
    type: 'Point',
    coordinates: [bbox[0], bbox[1]],
  })

  let suburb = '_OTHER'
  if (container && container.properties.name) {
    suburb = container.properties.name
  }

  const category = map.category

  emit([suburb, category], 1)
}