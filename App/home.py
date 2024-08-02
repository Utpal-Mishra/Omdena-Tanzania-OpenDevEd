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
        
print('\n\nNEW RUN\nLibraries Imported\n')

# ------------------------------------------------------------- #

# import one
# import two
# import three
# import four

# ------------------------------------------------------------- #

st.set_page_config(page_title="OpenDevEd", layout="wide")

#################################################################

msg = st.toast('**Welcome to Omdena OpenDevEd!!!**', icon='🎉')
time.sleep(2)
msg.toast('**Omdena-OpenDevEd Collaboration**', icon='🔥')

#################################################################
   
# @st.cache_data(experimental_allow_widgets=True)
def app():
        
    st.write("")
    col1, col2 = st.columns(2)

    with col1:
        st.image("Omdena.png")

    with col2:
        st.image('Tanzania.png', width = 130)

    st.title("Omdena - OpenDevEd")
    st.header("AI-Driven Temperature Analysis for Educational Environments in Tanzania")
        
    tab1, tab2 , tab3, tab4, tab5 = st.tabs(["About :information_source:", 
                                             "Locating Schools :school:", 
                                             "Weather Analysis :cloud:", 
                                             "Weather Report :chart:", 
                                             "Contact :phone:"])
    
    # Placeholder for Sidebar Content: sidebar_placeholder = st.sidebar.empty() 
           
    #################################################################
    
    with tab1: 
        
        # ------------------------------------------------------------- #
        
        # one.about()

        # ------------------------------------------------------------- #
        
        st.subheader("PROBLEM: \nIn countries with a hot climate, such as Tanzania, many schools experience classroom conditions characterized by extreme temperatures, which can severely impede the learning process and pose significant health risks to students. The primary challenge lies in the lack of detailed, actionable data regarding specific classroom features that influence indoor temperatures, such as roofing materials and the presence or absence of ceiling boards. Traditional methods for monitoring and improving these conditions often fall short because they do not provide the precise, localized information necessary for effective intervention.")
        st.subheader("Impact of the Problem: \n1. Ineffective Learning Environments \n2. Health Risks \n3. Inadequate Resource Allocation \n4. Barriers to Policy Implementation")
        st.subheader("GOAL: \nThe primary goal of this project is to develop an AI-driven predictive model using satellite imagery and environmental data to estimate indoor classroom temperatures in Tanzanian schools, enhancing learning environments and health safety. The model aims to determine temperature conditions based on observable features like roofing material, which need to be complemented with classroom specifications (including the presence of ceiling boards). The project unfolds over a 8+2-week cycle, each phase planned to ensure successful development and deployment: \n1. Data Collection and Resources \n2. Problem Definition and Model Development \n3. Temperature Range Detection \n4. Visualization and Reporting \n5. Flood Risk Assessment \n6. Deliverables and Optimization")
        
        st.divider()
        
        st.header("Gelocation of Schools in Tanzania")
        
        st.write("")    
            
        # ---------------------------------------------------------------------------------------------------------   
        
        ############################################################################################################ 
                
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
        # data.to_csv('data.csv', index = True)
        # data = pd.read_csv('data.csv')
        # st.dataframe(data)
        
        st.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), size = 50, zoom = 5)
               
        # ------------------------------------------------------------- #
        
    with tab2:
        
        # ------------------------------------------------------------- #
        
        # two.schools()
        
        # ------------------------------------------------------------- #
        
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

    # Main content area
    with tab2:
        
        address = 'Tanzania'
        geolocator = Nominatim(user_agent="four_square")
        location = geolocator.geocode(address)
        latitude = location.latitude
        longitude = location.longitude

        # Create a folium map
        Map = folium.Map(location=[latitude, longitude], zoom_start=6)

        # Add the selected tile layer
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

        # -------------------------------------------------
                
        # folium.TileLayer('cartodbdark_matter').add_to(Map)
        # folium_static(Map)
    
        ############################################################################################################
        
        # map = st.empty()
        
        st.write('')
        st.write('List of Regions: {}'.format(len(data['Region'].unique())))
        # st.text(data['Region'].unique())
        st.write('Total Schools: {}'.format(len(data['SchoolName'].unique())))
        
        ############################################################################################################
            
        # st.sidebar.image("Omdena.png")    
        
        # Adding a sidebar with select boxes
        st.sidebar.header('Select a Location: ')
        
        schoolMarkers = []   
        map = None
        # Custom CSS to position the text at the bottom right of the sidebar      
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
                        
                        # Add-ons
                        st.sidebar.divider()
                            
                        st.sidebar.header("Couldn't Find a School?")
                        
                        # st.sidebar.button("Reset", type="primary")
                        if st.sidebar.button("Add Location"): 
                            
                                name = st.sidebar.text_input("Add School Name")
                                lat = st.sidebar.slider("Select latitude", data['Latitude'].min(), data['Latitude'].max(), (latitude))
                                long = st.sidebar.slider("Select longitude", data['Longitude'].min(), data['Longitude'].max(), (longitude))

                                st.sidebar.write("Coordinates: ", lat, long) # name
                                # st.write(region, council, ward, ownership, lat, long)
                                
                                if st.sidebar.toggle("Integrate School Location"):
                                    
                                    newdata = data
                                    newdata.loc[len(data.index)] = [lat, long, region, council, ward, name, ownership]
                                    st.balloons()
                                    st.toast('New School Location Added!!!', icon='🎉')
                                    
                                    # icon = folium.features.CustomIcon('/content/drive/My Drive/Colab Notebooks/pushpin.png', icon_size=(30,30))
                                    folium.Marker([lat, long], popup = name, icon=folium.Icon(color = 'red', icon = "thumb-tack", prefix='fa')).add_to(Map)
                                    folium_static(Map, width = 1200, height = 500)
                                    
        
        ############################################################################################################                   
    
        
        # ------------------------------------------------------------- #                
    
    with tab3:
                                        
        # ------------------------------------------------------------- #
        
        # three.weatherAnalysis()
        
        # ------------------------------------------------------------- #
        
        BASEURL = "http://api.weatherapi.com/v1"
        # st.write("BASE URL: 'http://api.weatherapi.com/v1")
        APIKEY = "6bd51cc56e814b49a4b123504240407" # "316171a92c5d458c85735242213008"
        # st.write("API KEY: ------------------------------")
                            
        Region = []
        Council = []
        Ward = []
        Latitude = []
        Longitude = []
        WindSpeed = []
        WindDegree = []
        WindDirection = []
        Gust = []
        Pressure = []
        Precipitation = []
        Temperature = []
        Visibility = []
        Humidity = []
        Cloud = []
        UV = []
                                                
        try:
            for i in range(map.shape[0]):
                                                        
                # URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + str(map.Latitude[i]) + str(map.Longitude[i]) + "&aqi=yes"
                # URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + map['Ward'][i] + ', ' + map['Council'][i] + ', ' + map['Region'][i] + ', Tanzania' + "&aqi=yes"
                URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + ', ' + map['Ward'][i] + map['Council'][i] + map['Region'][i] + ', Tanzania' + "&aqi=yes"
                response = requests.get(URL) # HTTP request

                dt = response.json()

                Ward.append(map['Ward'][i])
                Council.append(map['Council'][i])
                Region.append(map['Region'][i])
                Latitude.append(str(map['Latitude'][i]))
                Longitude.append(str(map['Longitude'][i]))
                WindSpeed.append(str(dt['current']["wind_mph"]))
                WindDegree.append(str(dt['current']["wind_degree"]))
                WindDirection.append(dt['current']["wind_dir"])
                Gust.append(str(dt['current']["gust_mph"]))
                Pressure.append(str(dt['current']["pressure_mb"]))
                Precipitation.append(str(dt['current']["precip_mm"]))
                Temperature.append(str(dt['current']["feelslike_c"]))
                Visibility.append(str(dt['current']["vis_miles"]))
                Humidity.append(str(dt['current']["humidity"]))
                Cloud.append(str(dt['current']["cloud"]))
                UV.append(str(dt['current']["uv"]))

            status = pd.DataFrame({'Ward': Ward,
                                   'Council': Council,
                                   'Region': Region,
                                   'Latitude': Latitude,
                                   'Longitude': Longitude,
                                   'WindSpeed': WindSpeed,
                                   'WindDegree': WindDegree,
                                   'WindDirection': WindDirection,
                                   'Gust': Gust,
                                   'Pressure': Pressure,
                                   'Precipitation': Precipitation,
                                   'Temperature': Temperature,
                                   'Visibility': Visibility,
                                   'Humidity': Humidity,
                                   'Cloud': Cloud,
                                   'UV': UV})

            # print('Data Shape: ', status.shape)
            # st.dataframe(status.head(20))
                            
            # status.to_csv('status.csv', index = True)
            # status = pd.read_csv('status.csv')
                                                            
            ############################################################################################################
                                
            # Ensure that latitude, longitude, and temperature are numeric
            status['Latitude'] = pd.to_numeric(status['Latitude'], errors='coerce')
            status['Longitude'] = pd.to_numeric(status['Longitude'], errors='coerce')
            status['Temperature'] = pd.to_numeric(status['Temperature'], errors='coerce')
            # st.dataframe(status)
                              
            # Drop rows with missing or NaN values
            status = status.dropna(subset=['Latitude', 'Longitude', 'Temperature'])
                   
            heat_data = [[status['Latitude'][i], status['Longitude'][i], status['Temperature'][i]] for i in range(len(status))]
            # st.write(heat_data)
               
            # Add ESRI Satellite Tile Layer
            folium.TileLayer(
                tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
                attr='Esri',
                name='Esri Satellite',
                overlay=False,
                control=True
            ).add_to(Map)
                            
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
            
                # Add heatmap layer to the map
            HeatMap(heat_data).add_to(Map)
            # HeatMap(status).add_to(folium.FeatureGroup(name='Heat Map').add_to(Map))
                            
            cluster = MarkerCluster().add_to(Map)

            for i in range(len(status)):
                    folium.Marker(
                        location = [status['Latitude'][i], status['Longitude'][i]],
                        popup = status['Ward'][i] + status['Council'][i] + status['Region'][i],
                        # icon = folium.Icon(color = "green", icon = "ok-sign"),
                    ).add_to(cluster)       
                    
            # ***ADD TEMPERATURE LEGEND***
                
            # Map.add_child(hm)
            folium_static(Map, width = 1200, height = 500)   
            
            st.divider()    
            
        except:
                
            st.divider() 
            
        ############################################################################################################            
               
        w23 = pd.read_csv('weather2023.csv')
        w23['station_nm'] = w23['station_nm'].apply(lambda x: x.title())  
        w23['date'] = pd.to_datetime(w23['date'], format='%d-%m-%Y').dt.date
        w23['date'] = pd.to_datetime(w23['date'], errors='coerce')
               
        w22 = pd.read_csv('weather2022.csv')
        w22['station_nm'] = w22['station_nm'].apply(lambda x: x.title())  
        w22['date'] = pd.to_datetime(w22['date'], format='%d-%m-%Y').dt.date
        w22['date'] = pd.to_datetime(w22['date'], errors='coerce')
        
        w21 = pd.read_csv('weather2021.csv')
        w21['station_nm'] = w21['station_nm'].apply(lambda x: x.title())  
        w21['date'] = pd.to_datetime(w21['date'], format='%d-%m-%Y').dt.date
        w21['date'] = pd.to_datetime(w21['date'], errors='coerce')
        
        w20 = pd.read_csv('weather2020.csv')
        w20['station_nm'] = w20['station_nm'].apply(lambda x: x.title())  
        w20['date'] = pd.to_datetime(w20['date'], format='%d-%m-%Y').dt.date
        w20['date'] = pd.to_datetime(w20['date'], errors='coerce')
        
        w19 = pd.read_csv('weather2019.csv')
        w19['station_nm'] = w19['station_nm'].apply(lambda x: x.title())  
        w19['date'] = pd.to_datetime(w19['date'], format='%d-%m-%Y').dt.date
        w19['date'] = pd.to_datetime(w19['date'], errors='coerce')
        
        w = [w19, w20, w21, w22, w23]
        weatherdata = pd.concat(w, ignore_index=True)
   
        visuals = weatherdata[['date', 'temp', 'dwpt', 'rhum', 'prcp', 'wdir', 'wspd', 'pres']]       
        visuals = visuals.groupby('date').mean().reset_index()
              
        visuals['month'] = visuals['date'].dt.month 
        # # visuals['month'] = visuals['date'].apply(lambda x: int(x.split('-')[1].split('-')[0]))
        visuals['month_nm'] = visuals['date'].dt.strftime('%b')
        visuals['year'] = visuals['date'].dt.year
        # st.dataframe(visuals)  
        
        # variables = ['date', 'month', 'temp', 'dwpt', 'rhum', 'prcp', 'wdir', 'wspd', 'pres']
        
        ############################################################################################################
        
        # Function to map month to season
        def get_season(month):
            if month in [12, 1, 2]:
                return 'Winter'
            elif month in [3, 4, 5]:
                return 'Spring'
            elif month in [6, 7, 8]:
                return 'Summer'
            else:
                return 'Fall'
            
        # Add season column
        visuals['season'] = visuals['month'].apply(get_season)

        # Create Streamlit selectbox for filtering
        filter_option = st.selectbox('Select Time Frame', ['Year-wise', '6-Month-wise', 'Season-wise'])
        
        # Function to insert NaN values at year boundaries
        def boundaries(data):
            years = data['year'].unique()
            new_data = pd.DataFrame(columns = data.columns)
            for year in years:
                year_data = data[data['year'] == year]
                new_data = pd.concat([new_data, year_data, pd.DataFrame({col: [None] for col in data.columns})], ignore_index=True)
            return new_data
        
        # Filter data based on the selected option
        if filter_option == 'Year-wise':
            # Year-wise filter
            year = st.selectbox('Select Year', sorted(visuals['year'].unique()))
            filtered_data = visuals[visuals['year'] == year]
            
        elif filter_option == '6-Month-wise':
            # 6-Month-wise filter
            months = [(1, 6), (7, 12)]
            selected_months = st.selectbox('Select 6-Month Period', ['Jan-Jun', 'Jul-Dec'])
            start_month, end_month = months[0] if selected_months == 'Jan-Jun' else months[1]
            filtered_data = visuals[(visuals['month'] >= start_month) & (visuals['month'] <= end_month)]
            filtered_data = boundaries(filtered_data)
            
        elif filter_option == 'Season-wise':
            # Season-wise filter
            season = st.selectbox('Select Season', ['Winter', 'Spring', 'Summer', 'Fall'])
            filtered_data = visuals[visuals['season'] == season]
            filtered_data = boundaries(filtered_data)
                        
        # PLOT: Temperature and Precipitation Over Time
                
        # Plot 1F --------------------------------------------------------------------------------------------------
                
        # Create subplots with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['temp'], name = 'Temperature', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
        fig.add_trace(go.Bar(x = filtered_data['date'], y = filtered_data['prcp'], name = 'Precipitation', marker = dict(color = 'royalblue')), secondary_y = True)

        # Update layout
        fig.update_layout(height=700, width=1500, title_text='Temperature and Precipitation Over Time', xaxis_title='Date')
        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
        fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
        fig.update_yaxes(title_text='Precipitation (mm)', linewidth = 2, linecolor = 'black', secondary_y=True)
        st.plotly_chart(fig)
       
        st.divider()
        
        # ----------------------------------------------------------------------------------------------------------
        
        # PLOT: Temperature and Humidity Over Time
        
        # Plot 1A --------------------------------------------------------------------------------------------------
                
        # Create subplots with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['temp'], name = 'Temperature', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
        fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['rhum'], name = 'Humidity', marker = dict(color = 'royalblue')), secondary_y = True)

        # Update layout
        fig.update_layout(height=700, width=1500, title_text='Temperature and Humidity Over Time: To understand the Heat Index and Comfort Levels', xaxis_title='Date')
        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
        fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
        fig.update_yaxes(title_text='Humidity', linewidth = 2, linecolor = 'black', secondary_y=True)
        st.plotly_chart(fig)
       
        st.divider()
        
        # ----------------------------------------------------------------------------------------------------------
        
        # PLOT: Wind Speed and Wind Direction Over Time
        
        # Plot 1A --------------------------------------------------------------------------------------------------
                       
        # Create subplots with secondary y-axis
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['wspd'], name = 'Wind Speed (km/h)', mode ='lines', line=dict(color = 'firebrick')), secondary_y = False)
        fig.add_trace(go.Scatter(x = filtered_data['date'], y = filtered_data['wdir'], name = 'Wind Direction (°)', marker = dict(color = 'royalblue')), secondary_y = True)

        # Update layout
        fig.update_layout(height=700, width=1500, title_text='Wind Speed and Wind Direction Over Time: To understand Weather Patterns and Storm Tracking', xaxis_title='Date')
        fig.update_xaxes(rangeslider_visible = True, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
        fig.update_yaxes(showline = True, title_text='Wind Speed (km/h)', linewidth = 2, linecolor = 'black', secondary_y=False)
        fig.update_yaxes(title_text='Wind Direction (°)', linewidth = 2, linecolor = 'black', secondary_y=True)
        st.plotly_chart(fig)
       
        st.divider()
        
        # ----------------------------------------------------------------------------------------------------------
        
        
        # ------------------------------------------------------------- #          
                
    with tab4: 
        
        # ------------------------------------------------------------- #
        
        # four.contact()
        
        # ------------------------------------------------------------- #
        
        Region = []
        Council = []
        Ward = []
        Latitude = []
        Longitude = []
        WindSpeed = []
        WindDegree = []
        WindDirection = []
        Gust = []
        Pressure = []
        Precipitation = []
        Temperature = []
        Visibility = []
        Humidity = []
        Cloud = []
        UV = []
        
        if region and council:
                                          
            URL = "http://api.weatherapi.com/v1/forecast.json?key=6bd51cc56e814b49a4b123504240407&q=" + council + ", "  + region + ", Tanzania&days=7&aqi=yes&alerts=yes"
            
            # HTTP request
            response = requests.get(URL)
            # checking the status code of the request
            # if response.status_code == 200:
                                            
            # getting data in the json format
            # data = response.json()

            if response.status_code == 200:
                
                dt = response.json()
                
                st.write('')
                col1, col2 = st.columns(2)
                col1.metric(label = dt['location']['name'] + ', ' + dt['location']['region'], value = str(dt['current']['temp_c']) + " °C", delta = str(round(dt['current']['temp_c'] - dt['current']['feelslike_c'], 2)) + " °C")
                col2.image('https:' + dt['current']['condition']['icon'], width = 100) # col2.write(dt['current']['condition']['text']) # print(dt['current']["cloud"])
                    
                st.write('')
                    
                datetime_str = dt['location']['localtime']
                day = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%A")
                clock = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%H:%M")
                st.write(str(dt['forecast']['forecastday'][0]['day']['maxtemp_c']) + '/ ' + str(dt['forecast']['forecastday'][0]['day']['mintemp_c']) + ' Feels Like ' + str(dt['current']['feelslike_c']))
                st.write(day + str('/ ') + clock) # print(dt['current']['last_updated'])
                    
                st.write('')
                   
                tm = []
                temp = []
                prcp = []
                    
                # Forecasting: Present Day - Next 7 Days - D = 0-7
                for i in range(len(dt['forecast']['forecastday'])): # len(dt['forecast']['forecastday'])

                    for k in range(len(dt['forecast']['forecastday'][i]['hour'])):
                        
                        tm.append(datetime.strptime(dt['forecast']['forecastday'][i]['hour'][k]['time'], "%Y-%m-%d %H:%M"))
                        temp.append(dt['forecast']['forecastday'][i]['hour'][k]['temp_c']) # dt['forecast']['forecastday'][i]['hour'][k]['feelslike_c']
                        prcp.append(dt['forecast']['forecastday'][i]['hour'][k]["precip_in"])
                   
                
                X = pd.DataFrame({'time': tm, 'temp': temp, 'prcp': prcp})
                    
                # Create subplots with secondary y-axis
                fig = make_subplots(specs=[[{"secondary_y": True}]])
                fig.add_trace(go.Scatter(x = X['time'], y = X['temp'], name = 'Temperature', mode ='lines+markers', line=dict(color = 'firebrick')), secondary_y = False) #, text=[f"Humidity: {h}" for h in X['humidity']], hoverinfo='text+x+y')
                fig.add_trace(go.Bar(x = X['time'], y = X['prcp'], name = 'Precipitation', marker = dict(color = 'royalblue')), secondary_y = True)

                # Update layout
                fig.update_layout(height=500, width=1500, title_text='Temperature and Precipitation Over Time', xaxis_title='Date')
                fig.update_xaxes(rangeslider_visible = False, showline = True, linewidth = 2, linecolor = 'black', mirror = True)
                fig.update_yaxes(showline = True, title_text='Temperature (°C)', linewidth = 2, linecolor = 'black', secondary_y=False)
                fig.update_yaxes(title_text='Precipitation (in)', linewidth = 2, linecolor = 'black', secondary_y=True)
                  
                fig.add_trace(go.Scatter(x = [datetime.strptime(dt['location']['localtime'], "%Y-%m-%d %H:%M")], y = [dt['current']['temp_c']], name = 'Current Time', mode='markers',marker = dict(color = 'blue', size = 10)))
                st.plotly_chart(fig)
                 
                st.write('')
                    
                col1, col2 = st.columns(2)
                col1.metric(label = "Sunrise",       value = dt['forecast']['forecastday'][i]['astro']['sunrise'])
                col1.image('SunriseIcon.png', width = 150)
                col2.metric(label = "Sunset",        value = dt['forecast']['forecastday'][i]['astro']['sunset'])
                col2.image('SunsetIcon.png', width = 150)
                    
                st.write('')
                    
                col1, col2, col3, col4, col5 = st.columns(5)
                uv = {1: 'Low', 2: 'Low', 3: 'Moderate', 4: 'Moderate', 5: 'Moderate', 6: 'High', 7: 'High', 8: 'Very High', 9: 'Very High', 10: 'Very High', '11': 'Extreme'}
                col1.metric(label = "UV Index",      value = uv[dt['current']["uv"]])
                col1.image('UVIcon.png', width = 50)
                col2.metric(label = "Humidity",      value = str(dt['current']["humidity"]) + ' %')
                col2.image('HumidityIcon.png', width = 50)
                col3.metric(label = "Precipitation", value = str(dt['current']["precip_in"]) + ' in')
                col3.image('PrecipitationIcon.png', width = 50)
                col4.metric(label = "Pressure",      value = str(round(dt['current']["pressure_in"])) + ' inHg')
                col4.image('PressureIcon.png', width = 50)
                col5.metric(label = "Wind",          value = str(dt['current']["wind_mph"]) + ' mph')
                col5.image('WindIcon.png', width = 50)
               
                st.write('')
                            
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                col1.metric(label = "CO",    value = str(round(response.json()['current']["air_quality"]["co"], 2)))
                col2.metric(label = "NO2",   value = str(round(response.json()['current']["air_quality"]["no2"], 2)))
                col3.metric(label = "O3",    value = str(round(response.json()['current']["air_quality"]["o3"], 2)))
                col4.metric(label = "SO2",   value = str(round(response.json()['current']["air_quality"]["so2"], 2)))
                col5.metric(label = "PM2.5", value = str(round(response.json()['current']["air_quality"]["pm2_5"], 2)))
                col6.metric(label = "PM10",  value = str(round(response.json()['current']["air_quality"]["pm10"], 2)))

                st.write('')
                
                col1, col2, col3, col4, col5, col6 = st.columns(6)
                if 'alerts' in dt and "alert" in dt['alerts'] and len(dt['alerts']["alert"]) == 0:
                    col6.markdown('<p style="color:green;">NO ALERT</p>', unsafe_allow_html=True)
                else:
                    alerts = dt['alerts']["alert"]
                    alerts_str = ", ".join(alerts)  # Combine alerts into a single string
                    col1.markdown(f'<p style="color:red;">{alerts_str}</p>', unsafe_allow_html=True)
                   
                """
                note = ToastNotifier()
                note.show_toast("Weather Notifications", "Activated!!!")
                """
            
                ### WhatsApp Notification ---------------------------------------------------------------------------------------------
                
                update = "About Location\nCouncil:{}\nRegion : {}\nCountry: {}\nDate   : {}\nTime   : {}\n\nAbout Weather\nTemperature: {} °C\nPrecipitation: {} in\nHumidity   : {} %\nWind Speed : {} mph\nPressure   : {} inHg\n\nClouds     : {} \nHeat Index : {} °C\nDew Point  : {} °C\nVisibility : {} miles\nGust      : {} mph".format(
                    dt['location']['name'], 
                    dt['location']['region'], 
                    'Tanzania', 
                    datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%Y-%m-%d"),
                    datetime.strptime(datetime_str, "%Y-%m-%d %H:%M").strftime("%H:%M"), #dt['location']['localtime'], 
                    dt['current']['temp_c'], 
                    dt['current']["precip_in"],
                    dt['current']["humidity"],
                    dt['current']["wind_mph"], 
                    dt['current']["pressure_in"], 
                    dt['current']["condition"]['text'], 
                    dt['current']['heatindex_c'], 
                    dt['current']['dewpoint_c'], 
                    dt['current']["vis_miles"], 
                    dt['current']["gust_mph"])
                
                st.write('')
                st.write('')
                st.write('')
                
                account_sid = 'ACf653a498b5c1f653741c07592e091dba'
                auth_token = '34d9864c72c500a257260754c4aac9bc'
                # account_sid = os.environ["ACCOUNT_SID"]
                # auth_token = os.environ["AUTH_TOKEN"]
                client = Client(account_sid, auth_token)
                
                with st.form(key='whatsapp_form'):
                    user_number = st.text_input('Receive WhatsApp Notifications (Enter Number with Country Code):', placeholder = 'Format Ex: 353XXXXXXXXX')
                    submit_button = st.form_submit_button(label='Get Notifications')

                if submit_button:
                    
                    st.info('Notifications Activated for Next 3 Hours', icon="ℹ️")
                    
                    if user_number:
                        
                        try:
                            message = client.messages.create(
                            from_= 'whatsapp:+14155238886',
                            body = 'Live Weather Status\n\n' + update,
                            to = 'whatsapp:+' + str(user_number)
                            )
                            
                            message = client.messages.create(
                            from_= 'whatsapp:+14155238886',
                            body = 'Weather Forecasting:\nFor Temperature and Precipitation\n\n',
                            to = 'whatsapp:+' + str(user_number)
                            )
                            
                            time.sleep(1)
                            
                            current_time = datetime.strptime(datetime_str, "%Y-%m-%d %H:%M")
                            # Get the next three hours from the current time
                            time_intervals = [current_time + timedelta(hours=i) for i in range(3)]
                            
                            # Iterate through the time intervals and compare with the DataFrame times
                            for i in range(len(X)):
                                data_time = X['time'][i]
                                if (current_time.date() == data_time.date() and current_time.time() <= data_time.time() < time_intervals[-1].time()):
                                    # print(data_time.strftime("%H:%M"))
                                    message = client.messages.create(
                                    from_= 'whatsapp:+14155238886',
                                    body = "Date: " + str(data_time.date()) + "\nTime: " + str(data_time.time()) + "\nT: " + str(X['temp'][i]) + " °C\nP: " + str(X['prcp'][i]) + " in\n\n",
                                    to = 'whatsapp:+' + str(user_number)
                                    )
                                    
                            # st.success('Notifications on the way to your WhatsApp!!')
                            msg = st.toast('Notifications on the Way!!', icon='🎉')
                            time.sleep(1)
                            msg.toast('Notifications on the way!!', icon='🔥')
                            time.sleep(1)
                            msg.toast('Notifications on the Way!!', icon='🚀')
                            
                        except Exception as e:
                            st.error(f'Failed to Send Message: {e}')
                    else:
                        st.error('Please Enter a Valid WhatsApp Number.')
        
        # ------------------------------------------------------------- #
        
    with tab5: 
        
        # ------------------------------------------------------------- #
        
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
        
        # ------------------------------------------------------------- #
        
    #################################################################
        
