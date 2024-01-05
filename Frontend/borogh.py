from math import radians, sin, cos, sqrt, atan2
patrol_boro_list = ['PATROL BORO BKLYN NORTH', 'PATROL BORO BRONX',
                    'PATROL BORO MAN SOUTH', 'PATROL BORO BKLYN SOUTH',
                    'PATROL BORO QUEENS SOUTH', 'PATROL BORO QUEENS NORTH',
                    'PATROL BORO MAN NORTH', 'PATROL BORO STATEN ISLAND']

patrol_boro_coordinates = {
    'PATROL BORO BKLYN NORTH': (40.6782, -73.9442),
    'PATROL BORO BRONX': (40.8448, -73.8648),
    'PATROL BORO MAN SOUTH': (40.7128, -74.0060),
    'PATROL BORO BKLYN SOUTH': (40.6782, -73.9442),
    'PATROL BORO QUEENS SOUTH': (40.7282, -73.7949),
    'PATROL BORO QUEENS NORTH': (40.7282, -73.7949),
    'PATROL BORO MAN NORTH': (40.7831, -73.9712),
    'PATROL BORO STATEN ISLAND': (40.5795, -74.1502),
}

def get_patrol_borough(lat, lon):
    def haversine(lat1, lon1, lat2, lon2):
        R = 6371
        dlat = radians(lat2 - lat1)
        dlon = radians(lon2 - lon1)
        a = sin(dlat / 2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        distance = R * c
        return distance

    closest_borough = None
    min_distance = float('inf')

    for borough, coordinates in patrol_boro_coordinates.items():
        distance = haversine(lat, lon, *coordinates)
        if distance < min_distance:
            min_distance = distance
            closest_borough = borough
    
    return closest_borough