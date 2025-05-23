import pandas as pd
import folium
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

df = pd.read_csv('../../data/aq_data_230525_cleaned.csv')
bri_df = pd.read_csv('../../data/state_bri.csv')

#Getting average co-ordinates to approximately pin point the state
state_coords = df.groupby('state')[['longitude', 'latitude']].mean().reset_index()

#merging the co-ordinates to the df with bri category
bri_df_with_location =bri_df.merge(state_coords, on='state', how='left')

map = folium.Map(location=[bri_df_with_location['latitude'].mean(),bri_df_with_location['longitude'].mean()], zoom_start=6)

for index, row in bri_df_with_location.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"State: {row['state']}<br>Breathable Index: {row['BRI']}<br>Risk: {row['BRI_Category']}",
        icon=folium.Icon(color='lightgreen' if row['BRI_Category'] == 'Low Risk' else 'orange' if row['BRI_Category'] == 'Moderate Risk' else 'red')
    ).add_to(map)
    
map