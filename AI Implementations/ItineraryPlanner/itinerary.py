"""
High-level itinerary generator that wires everything together.
Main function: generate_itinerary(user_id, ...)
"""

from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from datetime import datetime
import calendar

from .recommender import filter_candidates, score_and_rank, mmr_select
from .utils import parse_date_range, cluster_by_distance
from . import storage


def _load_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path, encoding="latin1")


def _to_place_dicts(df: pd.DataFrame) -> List[Dict]:
    out = []
    for _, row in df.iterrows():
        d = row.to_dict()
        if 'poi_id' not in d:
            d['poi_id'] = str(d.get('name') or d.get('Event Name') or 'unknown').strip()
        d['description'] = d.get('description') or ""
        try:
            d['rating'] = float(d.get('rating', 0))
        except Exception:
            d['rating'] = 0.0
        out.append(d)
    return out


def _month_to_range(month_str: str, year: int = 2025):
    """
    Convert Month or Month-Range (e.g., 'October', 'March-April')
    into (start_date, end_date) datetime objects.
    """
    if not month_str or not isinstance(month_str, str):
        return None, None

    month_str = month_str.strip()
    parts = month_str.split("-")

    if len(parts) == 1:  # Single month
        month = parts[0].strip()
        try:
            m_idx = list(calendar.month_name).index(month.capitalize())
        except ValueError:
            return None, None
        start = datetime(year, m_idx, 1)
        end = datetime(year, m_idx, calendar.monthrange(year, m_idx)[1])
        return start, end

    elif len(parts) == 2:  # Range like March-April
        m1 = parts[0].strip()
        m2 = parts[1].strip()
        try:
            m1_idx = list(calendar.month_name).index(m1.capitalize())
            m2_idx = list(calendar.month_name).index(m2.capitalize())
        except ValueError:
            return None, None
        start = datetime(year, m1_idx, 1)
        end = datetime(year, m2_idx, calendar.monthrange(year, m2_idx)[1])
        return start, end

    return None, None


def _filter_events_by_date(events_df: pd.DataFrame, user_profile: dict) -> pd.DataFrame:
    """
    Filters events based on user's travel_dates vs event Month.
    """
    if "travel_dates" not in user_profile or not user_profile["travel_dates"]:
        return events_df  # no filtering

    try:
        user_start, user_end = parse_date_range(user_profile["travel_dates"])
    except Exception:
        return events_df

    keep_rows = []
    for _, row in events_df.iterrows():
        month_str = str(row.get("Month", "")).strip()
        ev_start, ev_end = _month_to_range(month_str, year=user_start.year)
        if ev_start and ev_end:
            if ev_start <= user_end and ev_end >= user_start:  # overlap
                keep_rows.append(row)

    return pd.DataFrame(keep_rows)


def _enrich_events_with_coords(events_df: pd.DataFrame, places_df: pd.DataFrame) -> pd.DataFrame:
    """
    If events lack coordinates, map them to nearest place in same district/town.
    """
    events = events_df.copy()
    places = places_df.copy()

    if 'district' in places.columns:
        places['district_lc'] = places['district'].astype(str).str.lower()
    if 'town' in places.columns:
        places['town_lc'] = places['town'].astype(str).str.lower()

    for idx, row in events.iterrows():
        lat = row.get('latitude') or row.get('lat') or None
        lon = row.get('longitude') or row.get('lon') or None
        if lat and lon:
            continue

        district = str(row.get('District', '')).lower()
        venue = str(row.get('Venue / Place', '')).lower()
        candidate = None

        if venue:
            mask = places['name'].astype(str).str.lower().str.contains(venue, na=False)
            if mask.any():
                candidate = places[mask].iloc[0]

        if candidate is None and district:
            mask = places['district_lc'] == district
            if mask.any():
                candidate = places[mask].iloc[0]

        if candidate is not None:
            events.at[idx, 'latitude'] = candidate.get('latitude')
            events.at[idx, 'longitude'] = candidate.get('longitude')

    return events


def generate_itinerary(
    user_id: str,
    user_profiles_csv: str = "data/itinerary/user_profiles.csv",
    places_csv: str = "data/itinerary/tourism_places.csv",
    events_csv: str = "data/itinerary/events.csv",
    days: int = 5,
    start_point: Optional[Tuple[float, float]] = None,
    max_per_day: int = 3
) -> Dict[str, Any]:
    """
    Generate a structured itinerary for a given user_id.
    """
    # Load user
    users_df = pd.read_csv(user_profiles_csv, encoding="latin1")
    user_row = users_df[users_df['user_id'].astype(str) == str(user_id)]
    if user_row.empty:
        raise ValueError(f"user_id {user_id} not found")
    user_profile = user_row.iloc[0].to_dict()

    # Load data
    places_df = pd.read_csv(places_csv, encoding="latin1")
    events_df = pd.read_csv(events_csv, encoding="latin1")

    # ✅ filter & enrich events
    events_df = _filter_events_by_date(events_df, user_profile)
    events_df = _enrich_events_with_coords(events_df, places_df)

    # Prep data for recommender
    places_list = _to_place_dicts(places_df)
    events_list = [r.to_dict() for _, r in events_df.iterrows()]

    # Get visited from storage + profile
    visited_from_storage = set(storage.get_user_visited_pois(user_id))
    visited_from_profile = set()
    if 'visited_pois' in user_profile and user_profile.get('visited_pois'):
        raw = str(user_profile.get('visited_pois'))
        splits = [p.strip() for p in raw.replace("|", ",").split(",") if p.strip()]
        visited_from_profile.update(splits)
    visited_ids = visited_from_storage.union(visited_from_profile)

    # Origin point
    origin = None
    if start_point:
        origin = start_point
    elif 'home_latitude' in user_profile and 'home_longitude' in user_profile:
        try:
            origin = (float(user_profile['home_latitude']), float(user_profile['home_longitude']))
        except Exception:
            origin = None
    if origin is None and places_list:
        origin = (float(places_list[0]['latitude']), float(places_list[0]['longitude']))

    # Candidate selection
    candidate_list = filter_candidates(user_profile, places_list, events_list, visited_ids)

    # Ranking
    scored = score_and_rank(candidate_list, user_profile, origin=origin)
    top_candidates = scored[:max(20, days * max_per_day * 2)]
    selected = mmr_select(top_candidates, k=days * max_per_day, lambda_param=0.75)

    # Prepare output
    selected_plain = []
    for s in selected:
        try:
            lat = float(s['latitude'])
            lon = float(s['longitude'])
        except Exception:
            continue
        selected_plain.append({
            'poi_id': s['poi_id'],
            'name': s.get('name') or s.get('Event Name'),
            'type': s.get('type', ''),
            'description': s.get('description') or s.get('Special About', ''),
            'latitude': lat,
            'longitude': lon,
            'kind': s.get('kind', 'place'),
            'accessibility': s.get('accessibility', ''),
            'rating': s.get('rating', 0)
        })

    clusters = cluster_by_distance(selected_plain, max_cluster_km=70.0)

    itinerary_days = []
    if len(clusters) > days:
        buckets = [[] for _ in range(days)]
        for i, cluster in enumerate(clusters):
            buckets[min(i, days - 1)].extend(cluster)
    else:
        buckets = clusters + [[] for _ in range(days - len(clusters))]

    for day_idx in range(days):
        items = buckets[day_idx][:max_per_day] if buckets[day_idx] else []
        itinerary_days.append({
            "day": day_idx + 1,
            "date": None,
            "items": items
        })

    itinerary = {
        "user_id": str(user_id),
        "created_at": datetime.utcnow().isoformat() + "Z",
        "days": itinerary_days,
        "meta": {
            "preferences": {
                "interests": user_profile.get('interests'),
                "budget": user_profile.get('budget'),
                "mobility_needs": user_profile.get('mobility_needs')
            }
        }
    }

    storage.save_itinerary(user_id, itinerary)
    return itinerary
