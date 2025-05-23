import pandas as pd

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
