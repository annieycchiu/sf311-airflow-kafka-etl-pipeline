# Third-party imports
import numpy as np
import pandas as pd
from PIL import Image
from sqlalchemy import create_engine


def load_image(image_path):
    """
    Load an image from the specified file path.

    Args:
      - image_path (str): Path to the image file.

    Returns:
      - PIL.Image: Loaded image from the specified file path.
    """
    image = Image.open(image_path)
    return image

def get_data_from_postgres(query, config):
    """
    Retrieve data from PostgreSQL database using SQLAlchemy.
    
    Args:
      - query (str): SQL query to retrieve data from the database.
      - config (dict): Dictionary containing PostgreSQL connection details (user, password, host, port, database).

    Returns:
      - pandas.DataFrame: DataFrame containing the retrieved data.
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
    Customize sorting of an array by considering a special value.

    Args:
      - array (numpy.ndarray or list): Input array to be sorted.
      - order (str): Sorting order ('asc' for ascending, 'desc' for descending).
      - special_val_pos (str): Position of the special value ('beginning' or 'end').
      - special_val (str): Special value to be considered (default: 'Others').

    Returns:
      - numpy.ndarray or list: Sorted array considering the special value based on the specified order and position.
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
