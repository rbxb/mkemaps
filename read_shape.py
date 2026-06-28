import geopandas as gpd

gdf = gpd.read_file("./data/2025/ParcelPolygonTax_2025.shp")

#ald_district = '3'
#gdf = gdf[gdf['DistrictNa'] == ald_district]

print(gdf.head())

gdf['LandArea'] = gdf.geometry.area
gdf['LandValuePerSqFt'] = gdf['TotalLandV'] / gdf['LandArea']
gdf = gdf.sort_values(by=['LandValuePerSqFt', 'TotalLandV'], ascending=False)

#gdf = gdf[:10]
#gdf = gdf.iloc[::10]

def format_address(row: gpd.GeoSeries) -> str:
	# StreetNumb
	# AlternateS
	# StreetNu_1
	# StreetDire
	# StreetName
	# StreetType
	address = f"{row['StreetNumb']} {row['StreetDire']} {row['StreetName']} {row['StreetType']}"
	return address

gdf['Address'] = gdf.apply(format_address, axis=1)

print(gdf[[
	'Taxkey',
	'LandValuePerSqFt',
	'Address',
]].head())

lvdf = gdf[[
	'Taxkey',
	'Address',
	'LandValuePerSqFt',
	'geometry',
]]

print(lvdf.head())

out_csv = './data/2025/land_value.csv'
lvdf.to_csv(out_csv)
print('Saved to', out_csv)