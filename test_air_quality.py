"""
Quick test script for the Air Quality API (api-ninjas.com).
Run this locally after getting your free API key from https://api-ninjas.com

Usage:
    python test_air_quality.py
"""

import json
import requests

# TODO: paste your own key here (never commit this to your repo!)
API_KEY = "0FyMTCw9PAJdVmnsp78HIRBDVPpRZnOuUsRyeRP4"

BASE_URL = "https://api.api-ninjas.com/v1/airquality"

# Pick a few cities to represent Denmark vs Germany
cities_to_test = [
    {"city": "Aalborg", "country": "Denmark"},
    {"city": "Copenhagen", "country": "Denmark"},
    {"city": "Berlin", "country": "Germany"},
    {"city": "Munich", "country": "Germany"},
]

headers = {"X-Api-Key": API_KEY}

for location in cities_to_test:
    response = requests.get(BASE_URL, headers=headers, params=location)

    if response.status_code == 200:
        data = response.json()
        overall_aqi = data.get("overall_aqi", "N/A")
        pm25 = data.get("PM2.5", {}).get("concentration", "N/A")
        no2 = data.get("NO2", {}).get("concentration", "N/A")

        print(f"{location['city']}, {location['country']}:")
        print(f"  Overall AQI: {overall_aqi}")
        print(f"  PM2.5: {pm25} µg/m³")
        print(f"  NO2:   {no2} µg/m³")
        print("  Full response:")
        print(json.dumps(data, indent=2))
        print()
    else:
        print(f"{location['city']}: request failed (status {response.status_code})")
        print(f"  Response: {response.text}")
        print()
