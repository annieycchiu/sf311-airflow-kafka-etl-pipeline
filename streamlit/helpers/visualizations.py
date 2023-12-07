# Third-party imports
import numpy as np
import folium
import plotly.graph_objects as go

# Local application/library specific imports
from .utils import customize_array_sort

# default colors for bar, line, pie plots
colors = ['#73afe1', '#667e6b', '#eee1d0', '#789b7c', '#a6def8']

    
def generate_color_list(colors, num):
    """
    Generate a list of colors based on the input list of colors. 
    If the length of the input color list is smaller than the input num, 
    it will loop from the beginning until the length of the colors matches the num.

    Args:
      - colors (list): List of color codes.
      - num (int): Number of colors to generate.

    Returns:
      - list: List containing generated colors based on the input list.
    """
    if num <= 0:
        return []

    input_colors_len = len(colors)
    result_colors = []
    index = 0

    while len(result_colors) < num:
        pos = index % input_colors_len
        result_colors.append(colors[pos])
        index += 1

    return result_colors

def plot_horizontal_stacked_bar_chart(df, colors=colors):
    """
    Plot a horizontal stacked bar chart representing request counts per police district and per service type.

    Args:
      - df (pandas.DataFrame): DataFrame containing information about request cases.
      - colors (list): List of color codes for the lines in the chart (default: 'colors'.)

    Returns:
      - go.Figure: A plotly Figure object representing request counts per police district and per service type.
    """
    df = df.groupby(['gp_police_district', 'gp_service_type'])['count'].sum().reset_index()
    
    police_dists = df['gp_police_district'].unique()
    ordered_police_dists = customize_array_sort(police_dists, order='desc', special_val_pos='beginning')

    service_types = df['gp_service_type'].unique()
    ordered_service_types = customize_array_sort(service_types, order='asc', special_val_pos='end')

    vals = []
    for i in range(len(ordered_service_types)):
        val = df[df['gp_service_type'] == ordered_service_types[i]]['count'].to_list()
        vals.append(val)
    
    data = []
    for i in range(len(ordered_service_types)):
        color = colors[i % len(colors)]
            
        trace = go.Bar(
            y=ordered_police_dists, 
            x=vals[i], 
            orientation='h',
            name=f'{ordered_service_types[i]}', 
            marker=dict(color=color))
        data.append(trace)

    title_txt = 'Request Type Count per Police District'

    layout = go.Layout(
        title=title_txt,
        barmode='stack',
        xaxis=dict(title='Request Count'),
        yaxis=dict(title='Police Districts'),
    )

    fig = go.Figure(data=data, layout=layout)

    return fig

def plot_multi_line_chart(df, category='gp_police_district', colors=colors):
    """
    Plot a multi-line chart representing request counts by a specified category per date.

    Args:
      - df (pandas.DataFrame): DataFrame containing information about request cases.
      - category (str): Category by which the data will be grouped (default: 'gp_police_district'.)
                        It can be either 'gp_police_district' or 'gp_service_type'.
      - colors (list): List of color codes for the lines in the chart (default: 'colors'.)

    Returns:
      - go.Figure: A plotly Figure object representing request counts by the specified category per date.
    """
    x_data = list(df['date'].unique())
    categories = df[category].unique()
    categories = customize_array_sort(categories, order='asc', special_val_pos='end')

    y_datas = []
    for i in range(len(categories)):
        y_data = df[df[category] == categories[i]]['count'].to_list()
        y_datas.append(y_data)

    data = []
    for i in range(len(categories)):
        color = colors[i % len(colors)]
        # Creating traces for each line
        trace = go.Scatter(x=x_data, y=y_datas[i], mode='lines', name=categories[i],line=dict(color=color))
        data.append(trace)

    # Layout configuration
    title_txt = ' '.join(word.capitalize() for word in category.split('_')[1:])

    layout = go.Layout(
        title=f'Request Counts by {title_txt} per Date',
        xaxis=dict(title='Date'), yaxis=dict(title='Counts'), 
        width=1000, height=500)

    # Creating the figure with data and layout
    fig = go.Figure(data=data, layout=layout)

    # Update layout to set width and height
    fig.update_layout(width=1000, height=500)

    return fig

def plot_pie_chart(df, category='gp_service_type', colors=colors):
    """
    Plot a pie chart to represent the percentage of service types or police districts.

    Args: 
      - df (pandas.DataFrame): DataFrame containing data to be plotted.
      - category (str): The category for which the pie chart is plotted.
                        It can be either 'gp_service_type' or 'gp_police_district' (default: 'gp_service_type'.)
      - colors (list): List of color codes used for the pie chart. Defaults to predefined colors (default: 'colors'.)
    
    Returns: 
      - go.Figure: A plotly Figure object representing the pie chart.
    """
    labels = list(df[category].unique())
    values = list(df.groupby(category)['count'].sum())
    colors = generate_color_list(colors, len(labels))

    # Creating the pie chart trace
    trace = go.Pie(labels=labels, values=values, marker=dict(colors=colors))

    # Creating the layout
    title_txt = ' '.join(word.capitalize() for word in category.split('_')[1:])

    layout = go.Layout(
        title=f'{title_txt} Percentage')

    # Creating the figure with data and layout
    fig = go.Figure(data=[trace], layout=layout)

    return fig

def plot_map(df):
    """
    Plot a San Francisco map to visualize hotspots of the request cases.
    
    Args:
      - df (pandas.DataFrame): DataFrame containing information about request cases.

    Returns:
      - folium.Map: A folium Map object visualizing hotspots of the request cases in San Francisco.
    """
    df = df[df['gp_police_district'] != 'Others']\
        .groupby(['gp_police_district', 'latitude', 'longitude'])['count'].sum().reset_index()
    
    sf_coordinate = [37.76,  -122.44]

    # create empty map zoomed in on San Francisco
    map = folium.Map(
        location=sf_coordinate, 
        zoom_start=12, 
        scrollWheelZoom=False, 
        tiles='cartodb positron')

    for i in range(df.shape[0]):
        dist = df.iloc[i]['gp_police_district'].capitalize()
        count = df.iloc[i]['count']
        lat = df.iloc[i]['latitude']
        lon = df.iloc[i]['longitude']
        location = [lat, lon]

        folium.Marker(
            location=location,
            popup=f"{dist}\ncounts: {count:,}",
            icon=None,
        ).add_to(map)

    return map 

