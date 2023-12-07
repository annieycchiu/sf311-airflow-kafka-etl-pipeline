# Third-party imports
import pandas as pd

# Local application/library specific imports
from .constants import service_mapping, police_mapping

def filter_dates(df, start_date, end_date):
    """
    Filter a DataFrame by date range.

    Args:
      - df (pandas.DataFrame): DataFrame containing date information.
      - start_date (str or datetime.date): Start date for filtering.
      - end_date (str or datetime.date): End date for filtering.

    Returns:
      - pandas.DataFrame: Filtered DataFrame within the specified date range.
    """
    df['date'] = pd.to_datetime(df['date']).dt.date
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return filtered_df

def group_infreq_police_district(x, chosen_police_districts):
    """
    Group infrequent police districts into 'Others'.

    Args:
      - x (str): Police district name.
      - chosen_police_districts (list): List of chosen police districts.

    Returns:
      - str: 'Others' if x is not in chosen_police_districts, otherwise returns x.
    """
    if x.capitalize() not in chosen_police_districts:
        return 'Others'
    return x

def group_infreq_service_type(x, chosen_service_types):
    """
    Group infrequent service types into 'Others'.

    Args:
      - x (str): Service type name.
      - chosen_service_types (list): List of chosen service types.

    Returns:
      - str: 'Others' if x is not in chosen_service_types, otherwise returns x.
    """
    if x not in chosen_service_types:
        return 'Others'
    return x

def prepare_user_filtered_data(
        df, # queried from PostgreSQL database
        chosen_dates, # user input
        chosen_police_districts, # user input
        chosen_service_types # user input
):
    """
    Generate a DataFrame based on user input for filtering.

    Args:
      - df (DataFrame): Queried data from PostgreSQL database.
      - chosen_dates (list): User-provided start and end dates for filtering.
      - chosen_police_districts (list): User-provided police districts for filtering.
      - chosen_service_types (list): User-provided service types for filtering.

    Returns:
      - DataFrame: DataFrame filtered based on user input.
    """

    # define all police distircts set
    all_police_districts = (
        'Bayview', 'Central', 'Ingleside', 'Mission', 'Northern', 
        'Park', 'Richmond', 'Southern', 'Taraval', 'Tenderloin')

    # define top service types set
    top_service_types = (
        'Abandoned Vehicle', 'Damaged Property', 'Encampments', 'General Request - MTA',
        'General Request - PUBLIC WORKS', 'Graffiti', 'Illegal Postings', 'Litter Receptacles',
        'Muni Employee Feedback', 'Muni Service Feedback', 'Noise Report', 'Parking Enforcement',
        'Rec and Park Requests', 'Sewer Issues', 'Sidewalk or Curb', 'Sign Repair',
        'Street Defects', 'Street and Sidewalk Cleaning', 'Streetlights', 'Tree Maintenance')
    
    # filter dataframe by chosen dates
    start_date = chosen_dates[0]
    end_date = chosen_dates[1]
    df = filter_dates(df, start_date, end_date)

    # group unchosen police districts into 'Others'
    if 'All' in chosen_police_districts:
        chosen_police_districts = all_police_districts
    df['gp_police_district'] = df['police_district'].apply(
        lambda x: group_infreq_police_district(x, chosen_police_districts))

    # group unchosen service types into 'Others'
    if 'All' in chosen_service_types:
        chosen_service_types = top_service_types
    df['gp_service_type'] = df['service_type'].apply(
        lambda x: group_infreq_service_type(x, chosen_service_types))

    return df

def generate_fastapi_input_data(
        service_type, 
        police_district, 
        service_mapping=service_mapping, 
        police_mapping=police_mapping
    ):
    """
    Generate input data for a FastAPI endpoint.

    Args:
      - service_type (str): Selected service type.
      - police_district (str): Selected police district.
      - service_mapping (dict): Mapping of service types to positions.
      - police_mapping (dict): Mapping of police districts to positions.

    Returns:
      - list: FastAPI input data formatted as a list of 31 values with True for 
              selected service type and police district, False otherwise.
    """
    pos1 = service_mapping[service_type]
    pos2 = police_mapping[police_district]

    # the format of the input data is a list of 31 values
    input_data = [False] * 31

    # Convert to 'True' for selected service type and police district
    input_data[pos1] = True
    input_data[pos2] = True

    return input_data