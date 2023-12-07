# Standard library imports
import os
from datetime import datetime, timedelta

# Third-party imports
from airflow import DAG
from airflow.operators.python_operator import PythonOperator

# Local application/library specific imports
from scripts.consumer import consume_messages_to_postgres
from operator_config import thresh


# define dag arguments
default_args = {
    'owner': 'annie',
    'start_date': datetime(2023, 11, 26),
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'execution_timezone': 'America/Los_Angeles',
}

# DAG: data consumption and loading
# DAG workflow:
#  Step 1. Consume the processed data from Kafka topic 
#  Step 2. Load the data into PostgreSQL database
with DAG(
    'sf_311_data_loading',
    default_args=default_args,
    description='Consume data from Kafka and upsert to PostgreSQL Database',
    schedule_interval='30 0 * * *', 
):

    # set this for airflow errors
    os.environ["no_proxy"] = "*"

    #  Step 1. Consume the processed data from Kafka topic 
    #  Step 2. Load the data into PostgreSQL database
    consume_data_ops = PythonOperator(
            task_id="consume_data",
            python_callable=consume_messages_to_postgres,
            op_kwargs={'thresh': thresh})

    # DAG workflow
    consume_data_ops
