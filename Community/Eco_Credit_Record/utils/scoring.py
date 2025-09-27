# This code for the utility to score eco-friendly actions
ACTION_SCORE_MAP = {
    "eco_hotel_stay": 50,
    "local_transport": 20,
    "buy_local_product": 10,
    "recycle_waste": 15,
    "plant_tree": 40,
    "guided_local_tour": 25,
    # fallback default
    "default": 5
}

def get_score(action: str) -> int:
    """
    Normalize action name and return eco_score.
    Accepts both pre-defined keys and tries fuzzy fallback.
    """
    key = action.strip().lower().replace(" ", "_")
    score = ACTION_SCORE_MAP.get(key)
    if score is not None:
        return score
    # try contains match
    for k in ACTION_SCORE_MAP:
        if k in key:
            return ACTION_SCORE_MAP[k]
    return ACTION_SCORE_MAP["default"]