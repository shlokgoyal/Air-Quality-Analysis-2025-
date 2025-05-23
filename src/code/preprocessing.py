import pandas as pd

#reading the dataset
df = pd.read_csv('../../data/aq_data_230525.csv')
df.sample(5)

#getting information
df.info()

#getting the statistical description of the data
df.describe()

#dropping the country column as there is only one country in the dataset
df.shape
df.drop(columns=['country'], inplace=True)
df.shape

#the last update column tells use about the time of the last update of the data
#converting the last updated column to datetime
df['last_update'] = pd.to_datetime(df['last_update'], format="%d-%m-%Y %H.%M")
df.info()

#checking for missing values
df.isnull().sum()
df.sample(10)

#getting names of the pollutants
df['pollutant_id'].unique()

#dealing with missing values without dropping the rows
pollutants = df['pollutant_id'].unique().tolist()

df.describe()
#since the we have the missing values in the rows we replace the missing values with the mean of the respective columns based on the pollutant_id


#Method 1: below is the code to impute means directly to the original dataframe
'''
pollutant_means = df.groupby('pollutant_id')[['pollutant_min','pollutant_max','pollutant_avg']].mean()
for pollutant in pollutants:
    df.loc[df['pollutant_id'] == pollutant, 'pollutant_min'] = df.loc[df['pollutant_id'] == pollutant, 'pollutant_min'].fillna(pollutant_means.loc[pollutant, 'pollutant_min'])
    df.loc[df['pollutant_id'] == pollutant, 'pollutant_max'] = df.loc[df['pollutant_id'] == pollutant, 'pollutant_max'].fillna(pollutant_means.loc[pollutant, 'pollutant_max'])
    df.loc[df['pollutant_id'] == pollutant, 'pollutant_avg'] = df.loc[df['pollutant_id'] == pollutant, 'pollutant_avg'].fillna(pollutant_means.loc[pollutant, 'pollutant_avg'])
'''

#Method 2: below is the code to impute means to a new dataframe using a function so that we can use it for other datasets as well

def impute_missing(df, pollutants):
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
    
    df = df.apply(impute_means, axis=1)
    return df    
    
#imputing the missing values
df_new = impute_missing(df, pollutants)
df.isnull().sum()

#checking the statistical description of the two dataframes
df1 = df.describe()
df2 = df_new.describe()    

#checking the difference between the output of the two methods
df2.subtract(df1)

#exporting the new dataframe to a csv file
df_new.to_csv('../../data/aq_data_230525_cleaned.csv', index=False)