import pandas as pd

def filter_csv():

    df = pd.read_csv('assault.csv')
    columns_to_keep = ['OCC_DATE','MCI_CATEGORY','LONG_WGS84','LAT_WGS84','PREMISES_TYPE']
    df_restricted_assault = df[columns_to_keep]
    df_restricted_assault.to_csv('output.csv', index=False)

    df = pd.read_csv('theft.csv')
    columns_to_keep = ['OCC_DATE','MCI_CATEGORY','LONG_WGS84','LAT_WGS84','PREMISES_TYPE']
    df_restricted_theft = df[columns_to_keep]
    df_restricted_theft.to_csv('output.csv', index=False)

    df = pd.read_csv('robbery.csv')
    columns_to_keep = ['OCC_DATE', 'MCI_CATEGORY', 'LONG_WGS84', 'LAT_WGS84','PREMISES_TYPE']
    df_restricted_robbary = df[columns_to_keep]
    df_restricted_robbary.to_csv('output.csv', index=False)

    all_crime_data = pd.concat([df_restricted_theft, df_restricted_assault,df_restricted_robbary])

    all_crime_data['DATE'] = pd.to_datetime(all_crime_data['OCC_DATE']).dt.strftime('%Y-%m-%d')
    columns_to_keep = ['DATE', 'MCI_CATEGORY', 'LONG_WGS84', 'LAT_WGS84','PREMISES_TYPE']
    all_crime_data = all_crime_data[columns_to_keep]
    return all_crime_data
