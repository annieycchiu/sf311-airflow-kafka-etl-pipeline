import numpy as np
import pandas as pd
from sqlalchemy import create_engine
from PIL import Image
import io


def load_image(image_path):
        image = Image.open(image_path)
        return image

def get_data_from_postgres(query, config):
    """
    Retrieve data from PostgreSQL database using SQLAlchemy.
    """
    # set database URL
    db_uri = f"postgresql://{config['user']}:{config['password']}@{config['host']}:{config['port']}/{config['database']}"
    # initiate PostgreSQL engine
    engine = create_engine(db_uri)
    # query data
    df = pd.read_sql(query, engine)
    # close the engine connection
    engine.dispose()  

    return df

def customize_array_sort(array, order, special_val_pos, special_val='Others'):
    """
    A customized sort function that can perform either ascending or descending sort and 
    insert special value in the beginning of the array or append it at the end.
    """
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
