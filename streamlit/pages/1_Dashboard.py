import os
from dotenv import load_dotenv
from sqlalchemy import create_engine

import pandas as pd
import plotly.express as px
import streamlit as st

# PostgreSQL configuration
def get_postgres_config():
    """
    Load Postgres configuration from environment variables.
    """
    return {
        "host": os.getenv("POSTGRE_HOST"),
        "port": os.getenv("POSTGRE_PORT"),
        "database": os.getenv("POSTGRE_DATABASE"),
        "user": os.getenv("POSTGRE_USER"),
        "password": os.getenv("POSTGRE_PASSWORD"),
    }

# retrieve data from PostgreSQL database using SQLAlchemy
def get_data_from_postgres(query, config):
    # set database URL
    db_uri = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    # initiate PostgreSQL engine
    engine = create_engine(db_uri)
    # query data
    df = pd.read_sql(query, engine)
    # close the engine connection
    engine.dispose()  

    return df

# Main App
def main():
   # set page configuration
    st.set_page_config(
        page_title='Request Dashboard', 
        page_icon=':bar_chart:', 
        layout='wide')
    
    # set page title
    st.title(':bar_chart: SF 311 Request Dashboard')

    # Query 1: retrive latest raw request data and display them in a table
    raw_data_q = """
        SELECT *
        FROM kafka_311_request
        ORDER BY updated_datetime DESC
        limit 100;
        """
    raw_data = get_data_from_postgres(raw_data_q, config)

    see_data = st.expander('Click here to see the latest requests 👉')
    with see_data:
        st.dataframe(data=raw_data.reset_index(drop=True))

    # Query 2: 

if __name__ == '__main__':
    # load secrets for PostgreSQL database connection
    load_dotenv(verbose=True)

    # get PostgreSQL database config
    config=get_postgres_config()

    main()