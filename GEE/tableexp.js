var filtered_region = S2.filterBounds(Rajasthan4);
var filtered_region_date = filtered_region.filterDate('2015-01-01', '2015-12-31');
var median_image = filtered_region_date.median();

var filtered_table = table.filter(ee.Filter.bounds(Rajasthan4))
var Rajasthan4 = ee.FeatureCollection(Rajasthan4);

Map.addLayer(median_image, vis2)
Map.addLayer(table)

Export.table.toDrive({
  collection: filtered_table,
  description: "Raj-solar-4",
  folder: "GEE_Data-newimp",
  fileNamePrefix: "Rajasthan_solar_4",
  fileFormat: "GeoJSON"
})