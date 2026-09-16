# Air Quality Comparison — Denmark vs Germany

A Streamlit app that compares real-time air quality between cities in Denmark and Germany, using the [Air Quality API](https://api-ninjas.com/api/airquality) (api-ninjas.com).

## What it does

- Lets you pick two cities from a dropdown (Aalborg, Copenhagen, Berlin, Munich)
- Shows the overall AQI for each city
- Breaks down 6 pollutants (CO, NO2, O3, SO2, PM2.5, PM10) in a grouped bar chart
- Explains why the overall AQI can be misleading: it's driven by whichever single pollutant scores highest — often ozone (O3) — even when other pollutants like NO2 and PM2.5 are much lower

## Limitation

The data is a single real-time snapshot, not an average. Ozone levels especially fluctuate with weather and time of day, so results can differ if you run the comparison on another day.

## Running locally

1. Clone this repo and `cd` into it
2. Create a virtual environment and install dependencies:
   
   pip install -r requirements.txt
   
3. Create a `.streamlit/secrets.toml` file with your own API key:
   
   API_NINJAS_KEY = "your_key_here"
   
4. Run the app:
   
   streamlit run app.py
   

## AI tools used

We used Claude to:

- Debug the API response structure and understand what drives the AQI value
- Write the app code
- Build the pollutant breakdown visualization with Plotly



## Team

Andreas Nørhave Vestergård, Andrei Busuioc, Anna Sanina, Mishel Licaj
