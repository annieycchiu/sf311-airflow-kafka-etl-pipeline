# Third-party imports
import joblib
import numpy as np
from fastapi import FastAPI


# initialize FastAPI instance for an API application
app = FastAPI()

# load trained model
clf = joblib.load('./models/random_forest_311_v2.joblib')


@app.post("/predict")
async def predict(data: dict):
    """
    Endpoint for making request resolved time range predictions.

    Args:
      - data (dict): Dictionary containing user input data.

    Returns:
      - dict: Dictionary containing the prediction result.
    """
    # convert the user input data into a numpy array and reshape it
    user_input = np.array(data['data']).reshape(1, -1)

    # make a prediction using the loaded model
    prediction = clf.predict(user_input)[0].split('-')[1].strip()

    return {"prediction": prediction}