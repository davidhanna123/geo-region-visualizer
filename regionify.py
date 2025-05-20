import pandas as pd
import geopandas as gpd
from shapely.geometry import Polygon, MultiPolygon
from fuzzywuzzy import process

# Load your bishop CSV
df = pd.read_csv('data/bishop_map_data.csv')

# Load Natural Earth Admin 1 boundaries shapefile
gdf = gpd.read_file('data/ne_10m_admin_1_states_provinces.shp')

# Prepare a lookup list for fuzzy matching from boundaries dataset
region_names = gdf['name'].tolist()

def match_region(region):
    # Fuzzy match with threshold for partial matches
    match, score = process.extractOne(region, region_names)
    if score > 65:
        return match
    return None

# Explode multiple regions per bishop to one region per row
df['regions'] = df['regions'].str.split(',')
df = df.explode('regions')
df['regions'] = df['regions'].str.strip()

# Match bishop regions to admin boundaries
df['matched_region'] = df['regions'].apply(match_region)

# Drop unmatched for now
df_matched = df.dropna(subset=['matched_region'])

# Join with polygons
merged = df_matched.merge(gdf, left_on='matched_region', right_on='name')

# Remove duplicates: keep only one row per bishop and region polygon
merged = merged.drop_duplicates(subset=['name_x', 'matched_region'])

# Keep only necessary columns and convert to GeoDataFrame
merged_gdf = gpd.GeoDataFrame(merged, geometry='geometry')

# Create properties with bishop name and original region
merged_gdf['properties'] = merged_gdf.apply(lambda row: {
    'bishop': row['name_x'],
    'region': row['regions']
}, axis=1)


if merged_gdf.crs is not None and merged_gdf.crs.to_string() != "EPSG:4326":
    merged_gdf = merged_gdf.to_crs(epsg=4326)


geojson = {
    "type": "FeatureCollection",
    "features": []
}

for _, row in merged_gdf.iterrows():
    geom = row.geometry.__geo_interface__
    feature = {
        "type": "Feature",
        "geometry": geom,
        "properties": {
            "bishop": row['name_x'],
            "region": row['regions']
        }
    }
    geojson["features"].append(feature)


import json
with open('data/bishops_regions.geojson', 'w') as f:
    json.dump(geojson, f)

print("GeoJSON file created: bishops_regions.geojson")
