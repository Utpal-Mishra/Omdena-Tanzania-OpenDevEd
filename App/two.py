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
        
print('Page 2: Libraries Imported')

# st.set_page_config(layout="wide")

#################################################################

def schools():
    
    if 'data' in st.session_state:
        
        data = st.session_state['data']
        
        address = 'Tanzania'
        geolocator = Nominatim(user_agent="four_square")
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude

        # Create a folium map
        Map = folium.Map(location=[latitude, longitude], zoom_start=6)
        
        # Create a list of tile layers
        tile_layers = {
            'Open Street Map': 'openstreetmap',
            'Stamen Terrain': 'Stamen Terrain',
            'Stamen Toner': 'Stamen Toner',
            'Stamen Watercolor': 'Stamen Watercolor',
            'CartoDB Positron': 'CartoDB positron',
            'CartoDB Dark Matter': 'CartoDB dark_matter',
            'Esri Satellite': 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}'
        }

        # Sidebar for tile layer selection
        selected_tile = st.sidebar.selectbox('Select Tile Layer', list(tile_layers.keys())) #, index=None, placeholder="Select Map Tile")
        
        if selected_tile == 'Esri Satellite':
            folium.TileLayer(
                tiles=tile_layers[selected_tile],
                attr='Esri',
                name='Esri Satellite',
                overlay=False,
                control=True
            ).add_to(Map)
        else:
            folium.TileLayer(tile_layers[selected_tile]).add_to(Map)
        
        # Optionally add other markers or layers
        Marker = folium.map.FeatureGroup()
        MousePosition().add_to(Map)
        Map.add_child(folium.LatLngPopup())
    
        # Add-ons -----------------------------------------
        tanzania_border = geopandas.read_file("./tanzania.geojson")
        folium.GeoJson(tanzania_border,
                       style_function=lambda feature: {
                            "color": "red",
                        }).add_to(Map)

        station_buffer = geopandas.read_file("./tanzania_buffer_05.geojson")
        folium.GeoJson(station_buffer,
                       style_function=lambda feature: {
                            "fillColor": "red",
                            "color": "red",
                            "weight": 5,
                        }).add_to(Map)
        
        folium.TileLayer('cartodbdark_matter').add_to(Map)
        folium_static(Map)
        
        st.write('')
        st.write('List of Regions: {}'.format(len(data['Region'].unique())))
        st.write('Total Schools: {}'.format(len(data['SchoolName'].unique())))
        
        ############################################################################################################
            
        # st.sidebar.image("Omdena.png")    
        
        st.sidebar.header('Select a Location: ')
           
        schoolMarkers = []   
        map = None
            
        region = st.sidebar.selectbox('Select Region', 
                                    tuple(sorted(set(list(data['Region'])))),
                                    index = None,
                                    placeholder = "Select Region",
                                    key = 's1')

        showPredict = False
        st.session_state.predictions = [0]*7
        
        if not region:
            
            st.info('Want to see what a Region can tell?', icon="ℹ️")  
        
        else:
            
            st.divider()
            
            st.write('Selected Regions: {}'.format(region))
            st.write('Total Councils: {}'.format(len(data[data['Region'] == region]['Council'].unique())))
            st.write('Total Wards: {}'.format(len(data[data['Region'] == region]['Ward'].unique())))
            st.write('Total Schools: {}'.format(len(data[data['Region'] == region]['SchoolName'].unique())))
          
            map = data.loc[(data['Region'] == region)]
            map = map.reset_index().drop('index', axis = 1)
            # st.dataframe(map)
            
            for idx, row in map.iterrows():
                    folium.Marker([row['Latitude'], 
                                row['Longitude']], 
                                popup = "School Name: " + row['SchoolName'] + ", Ownership Type: " + row['Ownership']).add_to(Map)
                    
            folium_static(Map, width = 1200, height = 500)
            
            st.divider()
            
            ############################################################################################################
                            
            council = st.sidebar.selectbox('Select Council', 
                                            tuple(sorted(set(list(data.loc[(data['Region'] == region)]['Council'])))),
                                            index=None,
                                            placeholder="Select Council")
                
            if not council:
            
                    st.info('Want to be a bit specific to Council?', icon="ℹ️") 
        
            else:  
                        
                st.write('Selected Regions: {}'.format(region))
                st.write('Selected Council: {}'.format(council))
                st.write('Total Wards: {}'.format(len(data[(data['Region'] == region) & (data['Council'] == council)]['Ward'].unique())))
                st.write('Total Schools: {}'.format(len(data[(data['Region'] == region) & (data['Council'] == council)]['SchoolName'].unique())))
                  
                map = data.loc[(data['Region'] == region) & (data['Council'] == council)]
                map = map.reset_index().drop('index', axis = 1)
                # st.dataframe(map)
                
                # latitude = map.loc[:, 'Latitude'].mean()
                # longitude = map.loc[:, 'Longitude'].mean()
                Map = folium.Map(location = [latitude, longitude], zoom_start = 6)
                Marker = folium.map.FeatureGroup()
                Marker.add_child(folium.CircleMarker([latitude, longitude],
                                                        radius = 7,
                                                        color = 'red',
                                                        #fill_color = 'red',
                                                        fill_opacity=0.7))
                Map.add_child(Marker)
                folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = "location-arrow", prefix='fa')).add_to(Map)
                MousePosition().add_to(Map)
            
                for idx, row in map.iterrows():
                        folium.Marker([row['Latitude'], 
                                    row['Longitude']], 
                                    popup = "School Name: " + row['SchoolName']).add_to(Map)

                folium_static(Map, width = 1200, height = 500)
                        
                st.divider()
                
                ############################################################################################################
                               
                ward = st.sidebar.selectbox('Select Ward', 
                                                tuple(sorted(set(list(data.loc[(data['Region'] == region) & (data['Council'] == council)]['Ward'])))),
                                                index=None,
                                                placeholder="Select Ward")
                    
                if not ward:
            
                    st.info('Want to Explore deep-down to Wards?', icon="ℹ️")  
        
                else:    
                                
                    st.write('Selected Regions: {}'.format(region))
                    st.write('Selected Council: {}'.format(council))
                    st.write('Selected Ward: {}'.format(ward))
                    st.write('Total Schools: {}'.format(len(data[(data['Region'] == region) & (data['Council'] == council) & (data['Ward'] == ward)]['SchoolName'].unique())))
                                
                    map = data.loc[(data['Region'] == region) & (data['Council'] == council) & (data['Ward'] == ward)]
                    map = map.reset_index().drop('index', axis = 1)
                    # st.dataframe(map)
                    
                    # latitude = map.loc[:, 'Latitude'].mean()
                    # longitude = map.loc[:, 'Longitude'].mean()
                    Map = folium.Map(location = [latitude, longitude], zoom_start = 6)
                    Marker = folium.map.FeatureGroup()
                    Marker.add_child(folium.CircleMarker([latitude, longitude],
                                                            radius = 7,
                                                            color = 'red',
                                                            #fill_color = 'red',
                                                            fill_opacity=0.7))
                    Map.add_child(Marker)
                    folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = "location-arrow", prefix='fa')).add_to(Map)
                    MousePosition().add_to(Map)
                    
                    for idx, row in map.iterrows():
                            folium.Marker([row['Latitude'], 
                                        row['Longitude']], 
                                        popup = "School Name: " + row['SchoolName']).add_to(Map)

                    folium_static(Map, width = 1200, height = 500)
                            
                    st.divider()
                
                    ############################################################################################################
                        
                    ownership = st.sidebar.selectbox('Select Ownership', 
                                                    tuple(sorted(set(list(data.loc[(data['Region'] == region) & (data['Council'] == council) & (data['Ward'] == ward)]['Ownership'])))),
                                                    index=None,
                                                    placeholder="Select Ownership")
                        
                    if ownership:   
                
                        st.write('Selected Regions: {}'.format(region))
                        st.write('Selected Council: {}'.format(council))
                        st.write('Selected Ward: {}'.format(ward))
                        st.write('Selected Ownership: {}'.format(ownership))
                        st.write('Total Schools: {}'.format(len(data[(data['Region'] == region) & (data['Council'] == council) & (data['Ward'] == ward) & (data['Ownership'] == ownership)]['SchoolName'].unique())))
                                   
                        map = data.loc[(data['Region'] == region) & (data['Council'] == council) & (data['Ward'] == ward) & (data['Ownership'] == ownership)]
                        map = map.reset_index().drop('index', axis = 1)
                        # st.dataframe(map)
                                                
                        # latitude = map.loc[:, 'Latitude'].mean()
                        # longitude = map.loc[:, 'Longitude'].mean()
                        Map = folium.Map(location = [latitude, longitude], zoom_start = 6)
                        Marker = folium.map.FeatureGroup()
                        Marker.add_child(folium.CircleMarker([latitude, longitude],
                                                                radius = 7,
                                                                color = 'red',
                                                                fill_color = 'red',
                                                                fill_opacity=0.7))
                        Map.add_child(Marker)
                        folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = "location-arrow", prefix='fa')).add_to(Map)
                        MousePosition().add_to(Map)
                                                
                        for idx, row in map.iterrows():
                                folium.Marker([row['Latitude'], 
                                            row['Longitude']], 
                                            popup = "School Name: " + row['SchoolName']).add_to(Map)

                        folium_static(Map, width = 1200, height = 500)
                        
                        st.sidebar.divider()
                            
                        st.sidebar.header("Couldn't Find a School?")
                        
                        if st.sidebar.button("Add Location"): 
                            
                                name = st.sidebar.text_input("Add School Name")
                                lat = st.sidebar.slider("Select latitude", data['Latitude'].min(), data['Latitude'].max(), (latitude))
                                long = st.sidebar.slider("Select longitude", data['Longitude'].min(), data['Longitude'].max(), (longitude))

                                st.sidebar.write("Coordinates: ", lat, long) 
                                
                                if st.sidebar.toggle("Integrate School Location"):
                                    
                                    newdata = data
                                    newdata.loc[len(data.index)] = [lat, long, region, council, ward, name, ownership]
                                    st.balloons()
                                    st.toast('New School Location Added!!!', icon='🎉')
                                    
                                    folium.Marker([lat, long], popup = name, icon=folium.Icon(color = 'red', icon = "thumb-tack", prefix='fa')).add_to(Map)
                                    folium_static(Map, width = 1200, height = 500)
                                    
            st.session_state['data'] = data
            st.session_state['region'] = region
            st.session_state['council'] = council
            st.session_state['map'] = map
            