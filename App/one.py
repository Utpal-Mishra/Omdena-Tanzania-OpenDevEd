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
        
print('Page 1: Libraries Imported')

# st.set_page_config(layout="wide")

#################################################################

def about():

        st.subheader("PROBLEM: \nIn countries with a hot climate, such as Tanzania, many schools experience classroom conditions characterized by extreme temperatures, which can severely impede the learning process and pose significant health risks to students. The primary challenge lies in the lack of detailed, actionable data regarding specific classroom features that influence indoor temperatures, such as roofing materials and the presence or absence of ceiling boards. Traditional methods for monitoring and improving these conditions often fall short because they do not provide the precise, localized information necessary for effective intervention.")
        st.subheader("Impact of the Problem: \n1. Ineffective Learning Environments \n2. Health Risks \n3. Inadequate Resource Allocation \n4. Barriers to Policy Implementation")
        st.subheader("GOAL: \nThe primary goal of this project is to develop an AI-driven predictive model using satellite imagery and environmental data to estimate indoor classroom temperatures in Tanzanian schools, enhancing learning environments and health safety. The model aims to determine temperature conditions based on observable features like roofing material, which need to be complemented with classroom specifications (including the presence of ceiling boards). The project unfolds over a 8+2-week cycle, each phase planned to ensure successful development and deployment: \n1. Data Collection and Resources \n2. Problem Definition and Model Development \n3. Temperature Range Detection \n4. Visualization and Reporting \n5. Flood Risk Assessment \n6. Deliverables and Optimization")
        
        st.divider()
        
        st.header("Gelocation of Schools in Tanzania")
        
        st.write("")    
        
        if 'data' not in st.session_state:
            
            data = pd.read_csv('primary_schools_2019.csv')
            data.drop(data.columns[[0]], axis=1, inplace=True)
            data.drop(data.columns[[10, 11]], axis=1, inplace=True)
            
            data.rename(columns = {'latitude': 'Latitude', 'longitude': 'Longitude', 
                                    'altitude': 'Altitude', 'geometry': 'Geometry', 
                                    'REGION': 'Region', 'COUNCIL': 'Council', 
                                    'WARD': 'Ward', 'SCHOOL_NAM': 'SchoolName',
                                    'OWNERSHIP': 'Ownership', 'REGISTRATI': 'Registration', 
                                    'TOTAL_POPULATION': 'TotalPopulation'}, inplace = True)
                
            data = data[['Latitude', 'Longitude', 'Region', 'Council', 'Ward', 'SchoolName', 'Ownership']]
                
            data['Region'] = data['Region'].apply(lambda x: x.title())
            data['SchoolName'] = data['SchoolName'].apply(lambda x: x.title())
                           
            st.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), size = 50, zoom = 5)
            
            st.session_state['data'] = data
                    