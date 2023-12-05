import pandas as pd
import plotly.graph_objects as go

from .utils import customize_array_sort

import numpy as np

def customize_array_sort(array, order, special_val_pos, special_val='Others'):
    if special_val in array:
        if order == 'asc':
            # Sort the array in ascending order (excluding the special value)
            sorted_array = np.sort(array[array != special_val])
        elif order == 'desc':
            # Sort the array in descending order (excluding the special value)
            sorted_array = np.sort(array[array != special_val])[::-1]
        
        if special_val_pos == 'beginning':
            # Combine special value at the beginning
            final_array = np.concatenate(([special_val], sorted_array))
        elif special_val_pos == 'end':
            # Combine special value at the beginning
            final_array = np.concatenate((sorted_array, [special_val]))

        return final_array
    
    elif special_val not in array:
        if order == 'asc':
            sorted_array = np.sort(array[array != special_val])
        elif order == 'desc':
            sorted_array = np.sort(array[array != special_val])[::-1]

        return sorted_array

def plot_horizontal_stacked_bar_chart(df):
    police_dists = df['gp_police_district'].unique()
    ordered_police_dists = customize_array_sort(police_dists, order='desc', special_val_pos='beginning')

    service_types = df['gp_service_type'].unique()
    ordered_service_types = customize_array_sort(service_types, order='asc', special_val_pos='end')

    vals = []
    for i in range(len(ordered_service_types)):
        val = df[df['gp_service_type'] == ordered_service_types[i]]['count'].to_list()
        vals.append(val)
    
    colors = ['#73afe1', '#a6def8', '#eee1d0', '#789b7c', '#667e6b']
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

    layout = go.Layout(
        barmode='stack',
        xaxis=dict(title='Request Count'),
        yaxis=dict(title='Police Districts')
    )

    fig = go.Figure(data=data, layout=layout)

    return fig