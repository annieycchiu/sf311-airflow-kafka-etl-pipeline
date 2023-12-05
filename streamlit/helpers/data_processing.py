import pandas as pd

all_police_districts = (
    'Bayview', 'Central', 'Ingleside', 'Mission', 'Northern', 
    'Park', 'Richmond', 'Southern', 'Taraval', 'Tenderloin')

top_service_types = (
    'Abandoned Vehicle', 'Damaged Property', 'Encampments', 'General Request - MTA',
    'General Request - PUBLIC WORKS', 'Graffiti', 'Illegal Postings', 'Litter Receptacles',
    'Muni Employee Feedback', 'Muni Service Feedback', 'Noise Report', 'Parking Enforcement',
    'Rec and Park Requests', 'Sewer Issues', 'Sidewalk or Curb', 'Sign Repair',
    'Street Defects', 'Street and Sidewalk Cleaning', 'Streetlights', 'Tree Maintenance')


def filter_dates(df, start_date, end_date):
    df['date'] = pd.to_datetime(df['date']).dt.date
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    return filtered_df

def group_infreq_police_district(x, chosen_police_districts):
    if x.capitalize() not in chosen_police_districts:
        return 'Others'
    return x

def group_infreq_service_type(x, chosen_service_types):
    if x not in chosen_service_types:
        return 'Others'
    return x

def prepare_user_filtered_data(
        df, # queried from PostgreSQL database
        chosen_dates, # user input
        chosen_police_districts, # user input
        chosen_service_types # user input
):
    # filter dataframe by chosen dates
    start_date = chosen_dates[0]
    end_date = chosen_dates[1]
    df = filter_dates(df, start_date, end_date)

    # group unchosen police districts into 'Others'
    if 'All' in chosen_police_districts:
        chosen_police_districts = all_police_districts
    df['gp_police_district'] = df['police_district'].apply(lambda x: group_infreq_police_district(x, chosen_police_districts))

    # group unchosen service types into 'Others'
    if 'All' in chosen_service_types:
        chosen_service_types = top_service_types
    df['gp_service_type'] = df['service_type'].apply(lambda x: group_infreq_service_type(x, chosen_service_types))

    return df