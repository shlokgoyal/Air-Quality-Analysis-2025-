import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import folium
import seaborn as sns

def map(input_data):
    #Function to preprocess
    def preprocess(df):
        df.drop(columns=['country'], inplace=True)
        df['last_update'] = pd.to_datetime(df['last_update'], format="%d-%m-%Y %H.%M")
        
        def impute_missing(df):
            pollutant_means = df.groupby('pollutant_id')[['pollutant_min','pollutant_max','pollutant_avg']].mean()
            
            def impute_means(row):
                pollutants = row['pollutant_id']
                if pd.isnull(row['pollutant_min']):
                    row['pollutant_min'] = pollutant_means.loc[pollutants, 'pollutant_min']
                if pd.isnull(row['pollutant_max']):
                    row['pollutant_max'] = pollutant_means.loc[pollutants, 'pollutant_max']
                if pd.isnull(row['pollutant_avg']):
                    row['pollutant_avg'] = pollutant_means.loc[pollutants, 'pollutant_avg']
                    
                return row
        
            return df.apply(impute_means, axis=1)
        df_imputed = impute_missing(df)
        return df_imputed

    #function to get the BRI values and categories
    def briCalc(df):
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
        return pivot_df
    
    #function to plot
    def state_map(df,bri_df):
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
            
        return map
    result1 = preprocess(input_data)
    result2 = briCalc(result1)
    result3 = state_map(result1, result2)
    return result3