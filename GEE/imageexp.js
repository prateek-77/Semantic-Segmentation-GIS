
var filtered_region = S2.filterBounds(Rajasthan4);
var filtered_region_date = filtered_region.filterDate('2015-01-01', '2015-12-31');
var median_image = filtered_region_date.median();


Map.addLayer(median_image, vis2)
Map.addLayer(table)


Export.image.toDrive({
  image: median_image.visualize(vis2),
  description: "Rajasthan-4",
  folder: "GEE_TIFFs",
  fileNamePrefix: "Rajsthan_image_4",
  region: Rajasthan4,
  maxPixels: 106355270,
  scale: 10,
  fileFormat: "GeoTIFF"  
})