from math import sin, cos, sqrt, atan2, radians


def straight_line_dist(loc1, loc2):
	# approximate radius of earth in km
	R = 6371.000

	lat1 = radians(loc1.lat)
	lon1 = radians(loc1.lon)
	lat2 = radians(loc2.lat)
	lon2 = radians(loc2.lon)

	dlon = lon2 - lon1
	dlat = lat2 - lat1

	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * atan2(sqrt(a), sqrt(1 - a))

	distance = R * c
	return distance
	print("Result:", distance)
	print("Should be:", 278.546, "km")