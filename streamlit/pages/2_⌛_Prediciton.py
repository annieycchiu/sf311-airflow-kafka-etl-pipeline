# Third-party imports
import requests
import streamlit as st

# Local application/library specific imports
from helpers.constants import service_mapping, police_mapping
from helpers.data_processing import generate_fastapi_input_data


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
        user_input = generate_fastapi_input_data(service_type, police_district)

        # make a POST request to the FastAPI endpoint for prediction
        response = requests.post("http://127.0.0.1:8000/predict", json={"data": user_input})
        
        # display prediction result
        if response.status_code == 200:
            result = response.json()
            st.write(
                f"<h4>Your requst is expected to be resolved: {result['prediction']}</h4>", 
                unsafe_allow_html=True)
        else:
            st.write(
                f"<h4>Failed to get prediction. Please check your input.</h4>", 
                unsafe_allow_html=True)

if __name__ == '__main__':
    main()