import pandas as pd
from sodapy import Socrata

def fetch_yesterday_data(url, app_token, sub_uri, data_limit, yesterday):
    """
    Fetch data from Socrata API and only retrieve yesterday's data.
    """
    # set up Socrata client
    client = Socrata(domain=url, app_token=app_token)

    # retrive data and convert to pandas dataframe
    results = client.get(dataset_identifier=sub_uri, limit=data_limit)
    results_df = pd.DataFrame.from_records(results)

    # only extract data updated yesterday to minimize data duplication
    mask = pd.to_datetime(results_df['updated_datetime']).dt.date == yesterday
    yesterday_df = results_df[mask]

    return yesterday_df

def df_to_csv(data_dir, yesterday, task_ids, **context):
    """
    Save pandas dataframe to csv file.
    """
    # retrieve pandas dataframe from the previous airflow task
    ti = context['ti']
    df = ti.xcom_pull(task_ids=task_ids)

    # define csv file directory and save the dataframe
    file_path = f"{data_dir}/{yesterday}"
    df.to_csv(f"{file_path}/sf_311.csv", index=False)


def extract_cols(data_dir, yesterday):
    """
    Extract necessary columns and rename them to match with PostgreSQL table.
    """
    # retrieve data from the raw data csv file
    file_path = f"{data_dir}/{yesterday}"
    df = pd.read_csv(f"{file_path}/sf_311.csv")

    # extract necessary columns
    cols = ['service_request_id', 'requested_datetime', 'updated_datetime', 'status_description',
            'agency_responsible', 'service_name', 'service_subtype', 'address', 'street', 
            'supervisor_district', 'neighborhoods_sffind_boundaries', 'police_district',
            'lat', 'long', 'source']
    df = df[cols]

    # rename columns to match with existing table in the database
    df = df.rename(columns={
        'service_request_id': 'request_id',
        'service_name': 'service_type',
        'neighborhoods_sffind_boundaries': 'neighborhood',
        'lat': 'latitude',
        'long': 'longitude'})
    
    return df