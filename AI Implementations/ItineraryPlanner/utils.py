"""
Utility helpers: Haversine distance, simple clustering by distance,
time helpers for parsing date ranges.
"""
from math import radians, sin, cos, asin, sqrt
from datetime import datetime
from typing import Tuple, List, Dict

def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Return distance between two lat/lon points in kilometers.
    Accepts degrees (e.g. '23.4497°' or 23.4497) — strips ° if present.
    """
    def _to_float(x):
        if x is None:
            return 0.0
        if isinstance(x, str):
            s = x.strip().replace("°", "")
            try:
                return float(s)
            except ValueError:
                return 0.0
        return float(x)

    lat1f, lon1f, lat2f, lon2f = map(_to_float, (lat1, lon1, lat2, lon2))
    # convert decimal degrees to radians
    lat1r, lon1r, lat2r, lon2r = map(radians, (lat1f, lon1f, lat2f, lon2f))

    dlon = lon2r - lon1r
    dlat = lat2r - lat1r
    a = sin(dlat/2)**2 + cos(lat1r) * cos(lat2r) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radius of Earth in kilometers
    return c * r

def parse_date_range(date_range: str) -> Tuple[datetime, datetime]:
    """
    Accepts strings like:
      '2025-10-15 to 2025-10-20' or '2025-10-15,2025-10-20'
    Returns (start_dt, end_dt)
    """
    if not date_range:
        raise ValueError("Empty date_range")
    sep = "to" if "to" in date_range else ","
    parts = [p.strip() for p in date_range.split(sep)]
    if len(parts) == 1:
        start = end = parts[0]
    else:
        start, end = parts[0], parts[1]
    fmt = "%Y-%m-%d"
    return datetime.strptime(start, fmt), datetime.strptime(end, fmt)

def cluster_by_distance(poIs: List[Dict], max_cluster_km: float = 50.0) -> List[List[Dict]]:
    """
    Simple greedy clustering:
      - Start with first POI as a cluster seed.
      - Add POIs whose distance to cluster centroid <= max_cluster_km.
    Returns list of clusters (each is a list of POI dicts).
    Note: This is simple and fast; if you need better grouping use DBSCAN.
    """
    clusters: List[List[Dict]] = []
    remaining = poIs.copy()

    while remaining:
        seed = remaining.pop(0)
        cluster = [seed]
        changed = True
        while changed:
            changed = False
            centroid_lat = sum(float(p['latitude']) for p in cluster) / len(cluster)
            centroid_lon = sum(float(p['longitude']) for p in cluster) / len(cluster)
            keep = []
            for p in remaining:
                d = haversine(centroid_lat, centroid_lon, p['latitude'], p['longitude'])
                if d <= max_cluster_km:
                    cluster.append(p)
                    changed = True
                else:
                    keep.append(p)
            remaining = keep
        clusters.append(cluster)
    return clusters
