from fastapi import FastAPI
import joblib
import numpy as np

app = FastAPI()

# load trained model
clf = joblib.load('./models/random_forest_311_v2.joblib')

# define endpoint for prediction
@app.post("/predict")
async def predict(data: dict):
    # convert the user input data into a numpy array and reshape it
    user_input = np.array(data['data']).reshape(1, -1)

    # make a prediction using the loaded model
    prediction = clf.predict(user_input)[0].split('-')[1].strip()

    return {"prediction": prediction}