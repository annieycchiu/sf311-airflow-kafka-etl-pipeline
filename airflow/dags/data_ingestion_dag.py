import os
from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator

from scripts.helper_functions import fetch_yesterday_data, df_to_csv, extract_cols
from scripts.producer import produce_csv_to_kafka
from operator_config import (
    yesterday, raw_data_dir, processed_data_dir, 
    sf_data_url, data_limit, sf_data_sub_uri, sf_data_app_token)


# define dag arguments
default_args = {
    'owner': 'annie',
    'start_date': datetime(2023, 11, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'execution_timezone': 'America/Los_Angeles',
}

# DAG: data ingestion and preprocessing 
# DAG workflow:
#  Step 1. Fetch San Francisco 311 data from Socrata API and save them to the raw data directory
#  Step 2. Perform data preprocessing on the raw data and save them to the processed data directory
#  Step 3. Produce the processed data to Kafka topic 
with DAG(
    dag_id="sf_311_data_ingestion",
    schedule='15 0 * * *', # scheduled to run at 00:15 AM every night
    description='Fetch, preprocess, and produce data to Kafka cluster',
    default_args=default_args) as dag:

    # set this for airflow errors
    os.environ["no_proxy"] = "*"  

    #  Step 1. Fetch San Francisco 311 data from Socrata API and save them to the raw data directory
    create_raw_data_dirs_ops = BashOperator(
        task_id="create_raw_data_dirs",
        bash_command=f"mkdir -p {raw_data_dir}/{yesterday}")

    fetch_data_ops = PythonOperator(
        task_id="fetch_data",
        python_callable=fetch_yesterday_data, 
        provide_context=True,
        op_kwargs={'url': sf_data_url,
                   'app_token': sf_data_app_token,
                   'sub_uri': sf_data_sub_uri,
                   'data_limit': data_limit,
                   'yesterday': yesterday})

    save_raw_data_ops = PythonOperator(
        task_id="save_raw_data",
        python_callable=df_to_csv,
        provide_context=True,
        op_kwargs={'data_dir': raw_data_dir,
                   'yesterday': yesterday,
                   'task_ids': 'fetch_data'})
    
    #  Step 2. Perform data preprocessing on the raw data and save them to the processed data directory
    extract_cols_ops = PythonOperator(
        task_id="extract_cols",
        python_callable=extract_cols,
        provide_context=True, 
        op_kwargs={'data_dir': raw_data_dir,
                   'yesterday': yesterday})
    
    create_processed_data_dirs_ops = BashOperator(
        task_id="create_processed_data_dirs",
        bash_command=f"mkdir -p {processed_data_dir}/{yesterday}")
    
    save_processed_data_ops = PythonOperator(
        task_id="save_processed_data",
        python_callable=df_to_csv,
        provide_context=True, 
        op_kwargs={'data_dir': processed_data_dir,
                   'yesterday': yesterday,
                   'task_ids': 'extract_cols'})
    
    #  Step 3. Produce the processed data to Kafka topic 
    produce_data_ops = PythonOperator(
        task_id="produce_data",
        python_callable=produce_csv_to_kafka,
        op_kwargs={'csv_path': f'{processed_data_dir}/{yesterday}/sf_311.csv'})
    

    # DAG workflow
    create_raw_data_dirs_ops >> fetch_data_ops >> save_raw_data_ops
    save_raw_data_ops >> extract_cols_ops >> create_processed_data_dirs_ops >> save_processed_data_ops
    save_processed_data_ops >> produce_data_ops