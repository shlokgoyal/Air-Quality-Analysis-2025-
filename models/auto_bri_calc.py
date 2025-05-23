import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

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