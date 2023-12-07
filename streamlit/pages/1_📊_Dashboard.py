# Standard library imports
import os
from datetime import date, timedelta

# Third-party imports
from dotenv import load_dotenv
import streamlit as st
from streamlit_folium import st_folium

# Local application/library specific imports
from helpers.utils import get_data_from_postgres
from helpers.data_processing import prepare_user_filtered_data
from helpers.queries import raw_data_query, main_query, new_metric_query, resolved_metric_query
from helpers.constants import police_district_list, service_types_list
from helpers.visualizations import (
    plot_horizontal_stacked_bar_chart, 
    plot_multi_line_chart, 
    plot_pie_chart, 
    plot_map)


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

    st.write('')
    st.write('')
    # Section 1: Latest Metrics

    st.write("<h4>🔍 Latest Metrics</h4>", unsafe_allow_html=True)

    st.write('')
    # Section 1-1: Six Metrics 

    col1, col2 = st.columns(2)
    with col1:
        st.write("<h5>New Request Counts</h5>", unsafe_allow_html=True)
    with col2:
        st.write("<h5>Resolved Request Counts</h5>", unsafe_allow_html=True)

    # retrieve data from PostgreSQL
    new_metric_data = get_data_from_postgres(new_metric_query, config)

    # retrieve data from PostgreSQL
    resolved_data = get_data_from_postgres(resolved_metric_query, config)

    col1, col2, col3, col4, col5, col6 = st.columns(6)
    with col1: 
        with col1:
            metric1 = sum(list(new_metric_data.iloc[0:1]['count']))
            st.metric('Yesterday', f'{metric1:,}')
        with col2:
            metric2 = sum(list(new_metric_data.iloc[0:7]['count']))
            st.metric('Past Week', f'{metric2:,}')
        with col3:
            metric3 = sum(list(new_metric_data.iloc[0:30]['count']))
            st.metric('Past Week', f'{metric3:,}')
        with col4:
            metric4 = sum(list(resolved_data.iloc[0:1]['count']))
            st.metric('Past Week', f'{metric4:,}')
        with col5:
            metric5 = sum(list(resolved_data.iloc[0:7]['count']))
            st.metric('Past Week', f'{metric5:,}')
        with col6:
            metric6 = sum(list(resolved_data.iloc[0:30]['count']))
            st.metric('Past Week', f'{metric6:,}')

    st.write('')
    # Section 1-2: Latest Raw Data 

    # retrieve data from PostgreSQL
    raw_data = get_data_from_postgres(raw_data_query, config)

    # define expander display
    expand_data = st.expander('Click here to see the latest requests 👉')
    with expand_data:
        st.dataframe(data=raw_data.reset_index(drop=True))

    st.write('')
    st.write('')
    # Section 2: Self Defined Dashboard

    st.write("<h4>🔍 Self Defined Dashboard</h4>", unsafe_allow_html=True)

    # Section 2-1: User Inputs
 
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
                                                 default=['Tenderloin', 'Mission', 'Northern', 'Ingleside'])
        chosen_police_districts = set(chosen_police_districts)
    
    # select service types
    with col3:
        chosen_service_types = st.multiselect('Request Types', options=service_types_list, 
                                              default=['Encampments', 'Street and Sidewalk Cleaning'])
        chosen_service_types = set(chosen_service_types)

    # Section 2-2: Display User Selected Data

    # retrieve data from PostgreSQL
    main_data = get_data_from_postgres(main_query, config)
    # filter data by user inputs
    user_chosen_df = prepare_user_filtered_data(main_data, chosen_dates, chosen_police_districts, chosen_service_types)

    st.write('')
    st.write('')
    # Plot 1: Map
    # Set up Streamlit layout to center the map
    _, col2, _ = st.columns([1, 5, 1])

    with col2:
        st.write('**Total Request Counts per Police District**')
        map = plot_map(user_chosen_df)
        st_folium(map, width=600, height=400) 

    # Plot 2: Horizonal Bar Plot
    col1, col2 = st.columns(2)
    with col1:
        horizontal_bar_fig = plot_horizontal_stacked_bar_chart(user_chosen_df)
        st.plotly_chart(horizontal_bar_fig)

    # Plot 3: Pie Plot
    with col2:
        pie_fig = plot_pie_chart(user_chosen_df, category='gp_service_type')
        st.plotly_chart(pie_fig)

    # Plot 4: Multi Line Plot
    multi_line_fig = plot_multi_line_chart(user_chosen_df, category='gp_police_district')
    st.plotly_chart(multi_line_fig)


if __name__ == '__main__':
    # load secrets for PostgreSQL database connection
    load_dotenv(verbose=True)

    # get PostgreSQL database config
    config=get_postgres_config()

    main()