import math

def haversine(lat1, lon1, lat2, lon2):
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    """
    # convert decimal degrees to radians 
    lon1, lat1, lon2, lat2 = map(math.radians, [lon1, lat1, lon2, lat2])

    # haversine formula 
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def recommend_ngos(donor_lat: float, donor_lon: float, ngos: list):
    """
    Recommend NGOs based on distance.
    ngos is a list of dictionaries or SQLAlchemy objects with lat/lon.
    """
    scored_ngos = []
    for ngo in ngos:
        if ngo.latitude and ngo.longitude:
            dist = haversine(donor_lat, donor_lon, ngo.latitude, ngo.longitude)
            scored_ngos.append({
                "ngo": ngo,
                "distance_km": round(dist, 2)
            })
            
    # Sort by distance
    scored_ngos.sort(key=lambda x: x["distance_km"])
    return scored_ngos[:10] # Top 10
