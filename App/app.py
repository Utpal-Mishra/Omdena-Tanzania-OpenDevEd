import home
import status
import streamlit as st

PAGES = {
    "Home": home,
    "Weather": status,
}

#st.sidebar.title('Navigation Bar')

# selection = st.sidebar.selectbox("Go to: \n", list(PAGES.keys()))
page = PAGES['Home']
page.app()