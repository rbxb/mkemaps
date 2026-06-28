import pyogrio
import geopandas as gpd

filename = "./data/2025/ParcelPolygonTax_2025.shp"

# Read the layer information and metadata properties
info = pyogrio.read_info(filename, layer="ParcelPolygonTax_2025")

print(info)

# Inspect the fields metadata for alternative names/aliases
for field in info["fields"]:
    print(field)