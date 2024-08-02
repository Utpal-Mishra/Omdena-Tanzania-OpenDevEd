# LIBRARIES

import streamlit as st
# st.set_page_config(layout="wide")
from streamlit_lottie import st_lottie
from streamlit_folium import folium_static
import geopandas

import requests # library to handle requests
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation
import calendar

# !conda install -c conda-forge geopy --yes
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values
import geocoder

import json # library to handle JSON files

# from pandas.io.json import json_normalize
from pandas import json_normalize # tranform JSON file into a pandas dataframe

# !conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library # Version 1
from folium.plugins import MousePosition
from folium.plugins import HeatMap # https://alcidanalytics.com/p/geographic-heatmap-in-python
# https://stackoverflow.com/questions/57676583/how-to-specify-the-colors-in-folium-heatmap
# https://python-bloggers.com/2020/12/how-to-make-stunning-interactive-maps-with-python-and-folium-in-minutes/
# https://www.kaggle.com/code/daveianhickey/how-to-folium-for-maps-heatmaps-time-data
from folium.plugins import MarkerCluster # https://python-visualization.github.io/folium/latest/user_guide/plugins/marker_cluster.html

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import time
from datetime import datetime, timedelta

# import geopandas as gpd
import folium
from folium.plugins import HeatMap
import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
from plotly.subplots import make_subplots

from twilio.rest import Client
import os

# Weather Icons
# https://www.iconfinder.com/
        
print('Page 4: Libraries Imported\n')

# st.set_page_config(layout="wide")

#################################################################

def contact():
    
    st.title('Send Streamlit SMTP Email 🚀')

    st.markdown("""**Enter Email Details and Share Your View/ Enquiry!**""")

    # Taking inputs
    email_sender   = st.text_input('From: ')
    email_receiver = st.text_input('To: ')
    subject        = st.text_input('Subject: ')
    body           = st.text_area('Body: ')

    # Hide the password input
    password = st.text_input('Password: ', type="password", disabled=True)  

    if st.button("Send Email"):
        try:
            msg = MIMEText(body)
            msg['From'] = email_sender
            msg['To'] = email_receiver
            msg['Subject'] = subject

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(st.secrets["email"]["gmail"], st.secrets["email"]["password"])
            server.sendmail(email_sender, email_receiver, msg.as_string())
            server.quit()

            st.success('Email Sent Successfully! 🚀')
        except Exception as e:
            st.error(f"Failed to Send Email: {e}")