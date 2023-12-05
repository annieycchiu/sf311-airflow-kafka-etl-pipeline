import requests
import streamlit as st
from helpers.constants import service_mapping, police_mapping


# generate input data for FastAPI endpoint
def generate_input_data(
        service_type, 
        police_district, 
        service_mapping=service_mapping, 
        police_mapping=police_mapping):
    
    pos1 = service_mapping[service_type]
    pos2 = police_mapping[police_district]

    # the format of the input data is a list of 31 values
    # only the selected service type and police district will display True, the other will display False
    input_data = [False] * 31
    input_data[pos1] = True
    input_data[pos2] = True

    return input_data

# Main App
def main():
    # set page configuration
    st.set_page_config(
        page_title='Resolved Time Prediction', 
        page_icon=':hourglass_flowing_sand:', 
        layout='wide')

    # set page title
    st.title(":hourglass_flowing_sand: Request Resolved Time Prediction")

    # get service type user input from a drop down list
    service_type = st.selectbox(
        "What is your request type?",
        list(service_mapping.keys()),
        index=None,
        placeholder="Select request type...",)
    
    # print out the chosen service type
    st.write('You request type is:', service_type)

    # get police district user input from a drop down list
    police_district = st.selectbox(
        "Which police district are you located?",
        list(police_mapping.keys()),
        index=None,
        placeholder="Select police district...",)
    
    # print out the chosen police district
    st.write('You police district is:', police_district)

    st.write('')
    st.write('')
    if service_type and police_district:
        user_input = generate_input_data(service_type, police_district)

        # make a POST request to the FastAPI endpoint for prediction
        response = requests.post("http://127.0.0.1:8000/predict", json={"data": user_input})
        
        # display prediction result
        if response.status_code == 200:
            result = response.json()
            st.write(f"Your requst is expected to be resolved: {result['prediction']}")
        else:
            st.write("Failed to get prediction. Please check your input.")

if __name__ == '__main__':
    main()