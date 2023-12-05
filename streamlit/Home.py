import streamlit as st

# Main App
def main():
    # set page configuration
    st.set_page_config(
        page_title='SF 311 Requests', 
        page_icon=':foggy:', 
        layout='wide')

    # set page title
    st.title(':foggy: SF 311 Requests')

if __name__ == '__main__':
    main()
