# Importing LIBRARIES

import streamlit as st
# st.set_page_config(layout="wide")

import requests # library to handle requests
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

import json # library to handle JSON files

# from pandas.io.json import json_normalize
from pandas import json_normalize # tranform JSON file into a pandas dataframe

# !conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library
# from streamlit_folium import st_folium # type: ignore

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

import geopandas as gpd

print('Libraries Imported')


# @st.cache_data(experimental_allow_widgets=True)
def app():
    
    ############################################################################################################
    
    status = pd.read_csv('status.csv') # read csv file using pandas
    # status. csv file contains features variables such as Latitude, Longitude, Place, Region, SchoolName with Weather Parameters
    status.drop(status.columns[[0]], axis=1, inplace=True)
    st.dataframe(status) # display dataframe
       
    ############################################################################################################
    
    # map = st.empty() # useful to overwrite a variable multiple times
    
    st.sidebar.header('Select a Location: ') # Adding a sidebar with select boxes    
    
    region = st.sidebar.selectbox('Select Region', 
                                  tuple(sorted(set(list(status['Region'])))), # values to given as a tuple or simply within parenthesis
                                  index=None, # ordering
                                  placeholder="Select Region") #default value in select box

    if region: # conditions gets valid when variable is initialized 
        map = status.loc[(status['Region'] == region)] # formating data just for selected region
        # st.dataframe(map) # display new dataframe
        st.map(map.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 7) # st.map() puts constraint on columns names for Latitude and Longitude thus, it has to be changed accordingly
        
app()