"""
Filtering, scoring and selection logic for itinerary planner.
"""

from typing import List, Dict, Tuple
from datetime import datetime
from .utils import haversine


def _normalize_rating(rating):
    try:
        return float(rating) / 5.0
    except Exception:
        return 0.5  # default midpoint


def relevance_score(poi: Dict, user_profile: Dict) -> float:
    """
    Very simple relevance scoring:
      +0.45 if poi.type matches user's interests
      +0.35 * normalized rating
      +0.20 if accessibility matches user's mobility needs
    """
    score = 0.0
    interests = user_profile.get("interests", "")
    interest_list = [i.strip().lower() for i in interests.split(",")] if interests else []
    poi_type = str(poi.get("type", "")).lower()

    if poi_type and any(it in poi_type for it in interest_list):
        score += 0.45

    score += 0.35 * _normalize_rating(poi.get("rating", 3.0))

    mobility = user_profile.get("mobility_needs", "") or ""
    acc = str(poi.get("accessibility", "")).lower()
    if mobility and mobility.strip().lower() in acc:
        score += 0.20

    return score


def filter_candidates(user_profile: Dict, places: List[Dict], events: List[Dict], visited_ids: set) -> List[Dict]:
    """
    Build candidate list from places + events.
    Excludes already visited IDs.
    Ensures events use 'Special About' as description.
    """
    candidates = []

    # ---- Places ----
    for p in places:
        pid = p.get("poi_id") or p.get("name")
        if pid in visited_ids:
            continue
        try:
            lat = float(str(p.get("latitude")).replace("°", ""))
            lon = float(str(p.get("longitude")).replace("°", ""))
        except Exception:
            continue  # skip invalid coords

        p_copy = p.copy()
        p_copy['poi_id'] = pid
        p_copy['latitude'] = lat
        p_copy['longitude'] = lon
        p_copy['kind'] = 'place'
        candidates.append(p_copy)

    # ---- Events ----
    for e in events:
        eid = e.get("event_id") or e.get("Event Name")
        if eid in visited_ids:
            continue

        lat = e.get("latitude") or e.get("lat")
        lon = e.get("longitude") or e.get("lon")

        try:
            if lat is not None and lon is not None:
                latf = float(str(lat).replace("°", ""))
                lonf = float(str(lon).replace("°", ""))
            else:
                continue  # skip if no coords
        except Exception:
            continue

        e_copy = e.copy()
        e_copy['poi_id'] = eid
        e_copy['latitude'] = latf
        e_copy['longitude'] = lonf
        e_copy['type'] = e_copy.get('Category', 'event')

        # ✅ Always pull description from "Special About"
        e_copy['description'] = e_copy.get('Special About', e_copy.get('description', ''))

        e_copy['kind'] = 'event'
        candidates.append(e_copy)

    return candidates


def score_and_rank(candidates: List[Dict], user_profile: Dict, origin: Tuple[float, float] = None) -> List[Tuple[Dict, float]]:
    """
    Compute relevance + proximity score for candidates.
    """
    scored = []
    for c in candidates:
        rel = relevance_score(c, user_profile)

        # Proximity bonus
        prox = 0.0
        if origin and c.get('latitude') is not None:
            d = haversine(origin[0], origin[1], c['latitude'], c['longitude'])
            prox = max(0.0, 1 - min(d / 200.0, 1.0))  # scale ~200 km

        score = 0.6 * rel + 0.35 * prox
        scored.append((c, score))

    return sorted(scored, key=lambda x: x[1], reverse=True)


def mmr_select(scored: List[Tuple[Dict, float]], k: int = 10, lambda_param: float = 0.7) -> List[Dict]:
    """
    Maximal Marginal Relevance (MMR) for diverse selection.
    """
    if not scored:
        return []

    candidates = [c for c, s in scored]
    scores = {c['poi_id']: s for c, s in scored}
    selected = []
    remaining = set(c['poi_id'] for c in candidates)

    def similarity(a, b):
        d = haversine(a['latitude'], a['longitude'], b['latitude'], b['longitude'])
        return max(0.0, 1 - min(d / 200.0, 1.0))

    # Start with highest score
    first = candidates[0]
    selected.append(first)
    remaining.remove(first['poi_id'])

    while remaining and len(selected) < k:
        best_candidate = None
        best_val = -float('inf')
        for pid in list(remaining):
            cand = next(c for c in candidates if c['poi_id'] == pid)
            relevance = scores.get(pid, 0.0)
            max_sim = max(similarity(cand, s) for s in selected) if selected else 0.0
            mmr_score = lambda_param * relevance - (1 - lambda_param) * max_sim
            if mmr_score > best_val:
                best_val = mmr_score
                best_candidate = cand

        if best_candidate is None:
            break
        selected.append(best_candidate)
        remaining.remove(best_candidate['poi_id'])

    return selected
