import os
from dotenv import load_dotenv

import streamlit as st
from datetime import date, timedelta

from helpers.utils import get_data_from_postgres
from helpers.data_processing import prepare_user_filtered_data
from helpers.visualizations import plot_horizontal_stacked_bar_chart
from helpers.queries import raw_data_query, main_query
from helpers.constants import police_district_list, service_types_list


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

# Main App
def main():
   # set page configuration
    st.set_page_config(
        page_title='Request Dashboard', 
        page_icon=':bar_chart:', 
        layout='wide')
    
    # set page title
    st.title(':bar_chart: SF 311 Request Dashboard')

    # Chart 1: Latest request table

    # retrieve data from PostgreSQL
    raw_data = get_data_from_postgres(raw_data_query, config)

    # define expander display
    expand_data = st.expander('Click here to see the latest requests 👉')
    with expand_data:
        st.dataframe(data=raw_data.reset_index(drop=True))

    # define columns for user inputs
    col1, col2, col3 = st.columns(3)
    
    # select dates
    with col1:
        a_year_ago = date.today() - timedelta(days=365)
        today = date.today()
        chosen_dates = st.slider('Dates', min_value=date(2021, 1, 1), max_value=date.today(), 
                                 value=(a_year_ago, today), format='YYYY-MM-DD')

    # select police districts
    with col2:
        chosen_police_districts = st.multiselect('Police Districts', options=police_district_list, 
                                                 default=['Bayview', 'Tenderloin'])
        chosen_police_districts = set(chosen_police_districts)
    
    # select service types
    with col3:
        chosen_service_types = st.multiselect('Request Types', options=service_types_list, 
                                              default=['Abandoned Vehicle', 'Encampments'])
        chosen_service_types = set(chosen_service_types)


    # Chart 2: Horizontal bar plot filtered by user inputs

    # retrieve data from PostgreSQL
    main_data = get_data_from_postgres(main_query, config)
    # filter data by user inputs
    user_chosen_df = prepare_user_filtered_data(main_data, chosen_dates, chosen_police_districts, chosen_service_types)
    # plot horizonal bar plot
    horizontal_bar_fig = plot_horizontal_stacked_bar_chart(user_chosen_df)

    st.plotly_chart(horizontal_bar_fig)


if __name__ == '__main__':
    # load secrets for PostgreSQL database connection
    load_dotenv(verbose=True)

    # get PostgreSQL database config
    config=get_postgres_config()

    main()