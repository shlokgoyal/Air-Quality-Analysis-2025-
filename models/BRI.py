
##calculating state-wise Breathable Air Quality Index (BAQI) based on the formula
# Pivot to have each pollutant as a column with average value per record
pivot_df = df.pivot_table(index=['state'], 
                          columns='pollutant_id', 
                          values='pollutant_avg', 
                          aggfunc='mean').reset_index()

# Fill missing pollutant columns with 0
for pollutant in ['PM2.5', 'PM10', 'NO2', 'SO2', 'CO', 'OZONE', 'NH3']:
    if pollutant not in pivot_df.columns:
        pivot_df[pollutant] = 0
    else:
        pivot_df[pollutant] = pivot_df[pollutant].fillna(0)

# Assign weights to pollutants
weights = {
    'PM2.5': 0.30,
    'PM10': 0.20,
    'NO2': 0.15,
    'SO2': 0.10,
    'CO': 0.10,
    'OZONE': 0.10,
    'NH3': 0.05
}

# Calculate weighted BRI per row
pivot_df['BRI'] = (
    pivot_df['PM2.5'] * weights['PM2.5'] +
    pivot_df['PM10'] * weights['PM10'] +
    pivot_df['NO2'] * weights['NO2'] +
    pivot_df['SO2'] * weights['SO2'] +
    pivot_df['CO'] * weights['CO'] +
    pivot_df['OZONE'] * weights['OZONE'] +
    pivot_df['NH3'] * weights['NH3']
)

# Now compute average BRI per state
state_bri = pivot_df.groupby('state')['BRI'].mean().sort_values(ascending=False)

#normalizing the BRI values to a 0-1 range
state_bri_normalized = (state_bri - state_bri.min()) / (state_bri.max() - state_bri.min())
state_bri_normalized.sort_values(ascending=False).head(10)

# Merge normalized BRI back to the pivot_df on 'state'
pivot_df = pivot_df.merge(state_bri_normalized.rename('normalized_BRI'), on='state', how='left')

# Multiply normalized BRI by 10 to scale to 0–10 range
pivot_df['BRI_score'] = pivot_df['normalized_BRI'] * 10

def classify_bri(score):
    if score < 3:
        return 'Low Risk'
    elif score < 6:
        return 'Moderate Risk'
    else:
        return 'High Risk'

pivot_df['BRI_Category'] = pivot_df['BRI_score'].apply(classify_bri)

#Exporting the data for BRI and insurance model
pivot_df.to_csv('../../data/state_bri.csv', index=False)


# create a folium map centered around the mean of latitude and longitude
with open("../../data/india_states.geojson", "r", encoding='utf-8') as f:
    india_states_geojson = json.load(f)
    
state_bri = pivot_df.groupby('state')['BRI_score'].mean().reset_index()

m = folium.Map(location=[22.9734, 78.6569], zoom_start=5, tiles="CartoDB positron")

folium.Choropleth(
    geo_data=india_states_geojson,
    name="choropleth",
    data=state_bri,
    columns=["state", "BRI_score"],
    key_on="feature.properties.NAME_1",  # Modify this based on your GeoJSON's property for state name
    fill_color="YlOrRd",
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name="Breathability Risk Index (0-10)"
).add_to(m)
folium.LayerControl().add_to(m)
m.save("india_bri_map.html")
m

state_name = list()
for state in india_states_geojson['features']:
    state_name.append(state['properties']['NAME_1'])

state_name