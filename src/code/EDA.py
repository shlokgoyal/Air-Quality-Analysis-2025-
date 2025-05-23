import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from matplotlib.ticker import PercentFormatter

#reading the csv file
df = pd.read_csv('../../data/aq_data_230525_cleaned.csv')
bri_safety = pd.read_csv('../../data/state_bri.csv')
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


# Plotting the the pollutant levels per state
state_pollutant = df.groupby(['state', 'pollutant_id']).size().unstack(fill_value=0)
#plotting barplot

state_category = bri_safety.groupby('state')['BRI_Category'].first().to_dict()


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
    

