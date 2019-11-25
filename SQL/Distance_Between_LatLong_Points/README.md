# Distance Between Lat-Long Points

SQL code to find the distance between two lat-long points on a globe.

Additional information can be found here:
[Calculating Distance Between Data Centers on a Globe](https://www.periscopedata.com/blog/calculating-distance-between-data-centers-on-a-globe)

	2 * 3960 * asin(sqrt((sin(radians(([latitude_2] - [latitude_1]) / 2)))

	   ^ 2 + cos(radians([latitude_1])) * cos(radians([latitude_2]))

	   * (sin(radians(([longitude_2] - [longitude_1]) / 2)))^ 2))

For area, see our blog post:
[Geographic Analysis in SQL: Measuring Polygon Area from Latitude and Longitude](https://www.periscopedata.com/blog/polygon-area-from-latitude-and-longitude-using-sql)