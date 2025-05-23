import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

#reading the csv file
df = pd.read_csv('../../data/aq_data_230525_cleaned.csv')
#getting infomation about the data
df.sample(10)
df.info()
df.describe()

#getting visual insight about min, max and avg levels of pollution by plotting mean and median for each value

cols = df.describe().columns[2:].to_list()

for i in cols:
    plt.figure(figsize=(10, 5))
    plt.title(f"Mean and Median of {i}")
    plt.axvline(df[i].mean(), color='red', linestyle='--', label='Mean')
    plt.axvline(df[i].median(), color='blue', linestyle='--', label='Median')
    sns.histplot(df[i])
    plt.xlabel(i)
    
    plt.legend()
    
    plt.show()
    
#plotting pollutant_avg based on pollutant_id to check for variation
sns.boxplot(x='pollutant_id', y='pollutant_avg', data=df, hue='pollutant_id', flierprops={'marker': 'o', 'color': 'black'})
plt.title('Pollutant Average by Pollutant ID')
plt.xlabel('Pollutant ID')
plt.ylabel('Pollutant Average')
plt.xticks(rotation=45)
plt.show()

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


#Exporting the data for BRI Visualisations and insurance claim analysis
pivot_df.to_csv('../../data/state_bri.csv', index=False)


# Plotting the the pollutant levels per state
state_pollutant = df.groupby(['state', 'pollutant_id']).size().unstack(fill_value=0)
#plotting barplot

state_category = pivot_df.groupby('state')['BRI_Category'].first().to_dict()


for state in state_pollutant.index:
    plt.figure(figsize=(12, 6))
    bri_cat = state_category.get(state, "Unknown")
    state_pollutant.loc[state].plot(kind='bar', color='blue')
    plt.title(f'Pollutant Levels in {state} - ({bri_cat})')
    plt.xlabel("Pollutants")
    plt.ylabel("Levels")
    plt.yscale("log")
    plt.xticks(rotation = 45)
    plt.show()