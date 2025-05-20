# Bishop Region Mapper

This project scrapes, processes, and visualizes information about bishops from the Coptic Orthodox Church website. The final output is a GeoJSON file that maps each bishop to their region, ready for display on an interactive map using Leaflet.js.

---

## 📦 Project Structure

- `scraper.py` – Scrapes bishop data from the Holy Synod website.
- `filterbish.py` – Parses and filters raw data into a cleaner format.
- `regionify.py` – Matches regions to geographic polygons and outputs a GeoJSON.
- `map.js` – Displays the GeoJSON data on an interactive map using Leaflet.js.
- `map.html` – HTML file for rendering the map.
- `data/bishops.csv` – Raw data after scraping.
- `data/bishop_map_data.csv` – Cleaned data after filtering.
- `data/bishops_regions.geojson` – Final output with geographic features.

---

## 🚀 Steps to Run

### ✅ Step 1: Scrape the Data

```bash
python scraper.py
```

- This script scrapes data from:
  https://copticorthodox.church/en/holysynod/synod-members/

- It collects each bishop's information from their individual cards.

- Output: data/bishops.csv

### ✅ Step 2: Filter and Clean

```bash
python filter_bish.py
```

- Parses and cleans data from bishops.csv.

- Standardizes region names and prepares the data for geolocation.

- Output: data/bishop_map_data.csv

### ✅ Step 3: Generate GeoJSON

```bash
python regionify.py
```

- Matches bishop regions to geographic boundaries using fuzzy matching.

- Converts matched regions into valid GeoJSON geometry.

- Output: data/bishops_regions.geojson (ready to be displayed on a map)

## 📝 Notes

- Ensure you have the required packages installed: pandas, geopandas, shapely, fuzzywuzzy, etc.

- Geo data comes from Natural Earth shapefiles. -https://www.naturalearthdata.com/
