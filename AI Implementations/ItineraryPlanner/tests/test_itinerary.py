"""
Unit test for the itinerary generator.
This test constructs small temporary CSVs, runs generate_itinerary, and asserts output.
Run with pytest from project root: `pytest AI Implementations/ItineraryPlanner/tests/test_itinerary.py`
"""
import os
import pandas as pd
from pathlib import Path
from ItineraryPlanner.itinerary import generate_itinerary

DATA_DIR = Path("data/itinerary")
DATA_DIR.mkdir(parents=True, exist_ok=True)

def _write_sample_csvs():
    user_profiles = pd.DataFrame([
        {"user_id": "1002", "interests": "Nature,Temple", "budget": "25000",
         "travel_dates": "2025-11-01 to 2025-11-05", "group_size": 5, "mobility_needs": "Wheelchair",
         "preferred_language": "Hindi", "meal_choice": "Non-Vegetarian", "visited_pois": "Baba Baidyanath Dham|Naulakha Temple|Nandan Pahar"}
    ])
    places = pd.DataFrame([
        {"name": "Hundru Falls", "poi_id": "hundru", "district": "Ranchi", "town": "Ranchi", "type": "waterfall", "latitude": 23.4497, "longitude": 85.6667, "description": "One of the highest waterfalls in Jharkhand", "rating": 4.2, "accessibility": "Partial"},
        {"name": "Patratu Valley", "poi_id": "patratu", "district": "Ramgarh", "town": "Patratu", "type": "nature", "latitude": 23.6524, "longitude": 85.2842, "description": "Picturesque valley", "rating": 4.7, "accessibility": "Limited"},
        {"name": "Netarhat", "poi_id": "netarhat", "district": "Latehar", "town": "Netarhat", "type": "hill", "latitude": 23.6, "longitude": 84.5, "description": "Queen of Chotanagpur", "rating": 4.5, "accessibility": "Wheelchair accessible"}
    ])
    events = pd.DataFrame([
        {"Event Name": "Jharkhand Food Festival", "Month": "October", "District": "Ranchi", "Venue / Place":"Morabadi Ground", "Duration":"1 day", "Category":"Food", "Special About":"Regional chefs"}
    ])
    user_profiles.to_csv(DATA_DIR / "user_profiles.csv", index=False)
    places.to_csv(DATA_DIR / "tourism_places.csv", index=False)
    events.to_csv(DATA_DIR / "events.csv", index=False)

def test_generate_itinerary_basic():
    _write_sample_csvs()
    itin = generate_itinerary(user_id="1002",
                              user_profiles_csv=str(DATA_DIR / "user_profiles.csv"),
                              places_csv=str(DATA_DIR / "tourism_places.csv"),
                              events_csv=str(DATA_DIR / "events.csv"),
                              days=3,
                              max_per_day=2)
    assert 'days' in itin
    assert len(itin['days']) == 3
    # check that previously visited POIs are not present
    visited_names = {"Baba Baidyanath Dham", "Naulakha Temple", "Nandan Pahar"}
    found = False
    for d in itin['days']:
        for item in d['items']:
            assert item['poi_id'] not in visited_names
            found = True
    assert found is True
