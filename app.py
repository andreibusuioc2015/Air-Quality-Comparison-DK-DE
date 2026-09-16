import pandas as pd
import plotly.express as px
import requests
import streamlit as st

st.set_page_config(page_title="Air Quality: Denmark vs Germany", page_icon="🌍")

st.title("🌍 Air Quality Comparison")
st.write(
    "Compare real-time air quality between cities in Denmark and Germany. "
    "Data comes from the Air Quality API (api-ninjas.com)."
)

# Cities available for comparison — feel free to add more later
CITIES = {
    "Aalborg (Denmark)": {"city": "Aalborg", "country": "Denmark"},
    "Copenhagen (Denmark)": {"city": "Copenhagen", "country": "Denmark"},
    "Berlin (Germany)": {"city": "Berlin", "country": "Germany"},
    "Munich (Germany)": {"city": "Munich", "country": "Germany"},
}

POLLUTANTS = ["CO", "NO2", "O3", "SO2", "PM2.5", "PM10"]

API_URL = "https://api.api-ninjas.com/v1/airquality"


@st.cache_data(ttl=600)  # cache for 10 minutes so we don't hammer the API
def fetch_air_quality(city: str, country: str):
    """Fetch air quality data for a city. Returns dict or None on failure."""
    headers = {"X-Api-Key": st.secrets["API_NINJAS_KEY"]}
    params = {"city": city, "country": country}

    try:
        response = requests.get(API_URL, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException:
        return None


col1, col2 = st.columns(2)

with col1:
    city_a_label = st.selectbox("First city", list(CITIES.keys()), index=0)

with col2:
    city_b_label = st.selectbox("Second city", list(CITIES.keys()), index=2)

st.divider()

city_a = CITIES[city_a_label]
city_b = CITIES[city_b_label]

data_a = fetch_air_quality(city_a["city"], city_a["country"])
data_b = fetch_air_quality(city_b["city"], city_b["country"])

# Handle the "API doesn't return data" requirement from the assignment
if data_a is None or data_b is None:
    st.error(
        "⚠️ Couldn't retrieve air quality data right now. "
        "The API might be temporarily unavailable — please try again in a moment."
    )
else:
    st.success("Data loaded successfully!")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(f"{city_a_label} — Overall AQI", data_a["overall_aqi"])
    with col2:
        st.metric(f"{city_b_label} — Overall AQI", data_b["overall_aqi"])

    st.subheader("Pollutant breakdown")

    # Build a tidy dataframe: one row per (city, pollutant) for a grouped bar chart
    rows = []
    for label, data in [(city_a_label, data_a), (city_b_label, data_b)]:
        for pollutant in POLLUTANTS:
            rows.append({
                "City": label,
                "Pollutant": pollutant,
                "Sub-AQI": data[pollutant]["aqi"],
                "Concentration (µg/m³)": data[pollutant]["concentration"],
            })
    df = pd.DataFrame(rows)

    fig = px.bar(
        df,
        x="Pollutant",
        y="Sub-AQI",
        color="City",
        barmode="group",
        title="Sub-AQI per pollutant (higher = worse)",
    )
    st.plotly_chart(fig, use_container_width=True)

    st.caption(
        "**What this shows:** the overall AQI is simply the highest sub-AQI among "
        "these six pollutants. A city can have a high overall AQI because of one "
        "pollutant (often ozone) even if its other pollutants — like traffic-related "
        "NO2 and PM2.5 — are much lower than a city with a lower overall AQI."
    )

    st.caption(
        "**Limitation:** this data is a single real-time snapshot, not a historical "
        "average. Ozone levels especially can swing a lot with weather and time of day, "
        "so re-running this comparison on a different day may give different results."
    )
