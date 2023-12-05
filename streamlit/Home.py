import streamlit as st

from helpers.utils import load_image

# Main App
def main():
    # set page configuration
    st.set_page_config(
        page_title='SF 311 Requests', 
        page_icon=':foggy:', 
        layout='wide')

    # set page title
    st.title(':foggy: SF 311 Requests')

    # display architecture diagram
    st.write("<h3 style='text-align: center;'>Architecture Diagram</h3>", unsafe_allow_html=True)
    image_path = 'assets/images/SF_311_Architecture.png'
    image = load_image(image_path)
    st.image(image, caption='Streaming Data ETL Pipeline')

if __name__ == '__main__':
    main()

# python -m streamlit run /Home.py 
