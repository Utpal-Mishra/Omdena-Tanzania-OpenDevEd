# RESOURCES
# https://docs.streamlit.io/develop/api-reference
# https://www.earthdatascience.org/tutorials/introduction-to-leaflet-animated-maps/
# *https://python-visualization.github.io/folium/latest/user_guide/map.html
# *https://python-visualization.github.io/folium/latest/user_guide/plugins/featuregroup_subgroup.html
# *https://python-visualization.github.io/folium/version-v0.10.1/modules.html
# https://openweathermap.org/current

###############################################################################################################

# LIBRARIES

import streamlit as st
# st.set_page_config(layout="wide")
from streamlit_lottie import st_lottie
from streamlit_folium import folium_static

import requests # library to handle requests
import numpy as np # library to handle data in a vectorized manner
import random # library for random number generation

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

# import geopandas as gpd
import folium
from folium.plugins import HeatMap
import plotly.express as px
import plotly.graph_objects as go


st.set_page_config(page_title="OpenDevEd") #, layout="wide")

print('Libraries Imported')

###############################################################################################################

st.toast('Welcome to Omdena OpenDevEd!!!', icon='🎉')

###############################################################################################################

# @st.cache_data(experimental_allow_widgets=True)
def app():
    
    st.write("")
            
    st.title("OMDENA OpenDevEd")
    st.header("AI-Driven Temperature Analysis for Educational Environments in Tanzania")
        
    tab1, tab2 , tab3= st.tabs(["About", "Locating Schools", "Weather Analysis"])
    
    ###########################################################################################################
    
    with tab1: 
        
        st.subheader("PROBLEM: \nIn countries with a hot climate, such as Tanzania, many schools experience classroom conditions characterized by extreme temperatures, which can severely impede the learning process and pose significant health risks to students. The primary challenge lies in the lack of detailed, actionable data regarding specific classroom features that influence indoor temperatures, such as roofing materials and the presence or absence of ceiling boards. Traditional methods for monitoring and improving these conditions often fall short because they do not provide the precise, localized information necessary for effective intervention.")
        st.subheader("Impact of the Problem: \n1. Ineffective Learning Environments \n2. Health Risks \n3. Inadequate Resource Allocation \n4. Barriers to Policy Implementation")
        st.subheader("GOAL: \nThe primary goal of this project is to develop an AI-driven predictive model using satellite imagery and environmental data to estimate indoor classroom temperatures in Tanzanian schools, enhancing learning environments and health safety. The model aims to determine temperature conditions based on observable features like roofing material, which need to be complemented with classroom specifications (including the presence of ceiling boards). The project unfolds over a 8+2-week cycle, each phase planned to ensure successful development and deployment: \n1. Data Collection and Resources \n2. Problem Definition and Model Development \n3. Temperature Range Detection \n4. Visualization and Reporting \n5. Flood Risk Assessment \n6. Deliverables and Optimization")
        
        st.divider()
        
        st.header("Gelocation of Schools in Tanzania")
        
        st.write("")    
            
        # ---------------------------------------------------------------------------------------------------------   
        
        ############################################################################################################ 
        
        '''
        f = open('primary_schools_2019.geojson', encoding='utf-8')

        # returns JSON object as a dictionary
        dt = json.load(f)

        Region = []
        Council = []
        Ward = []
        SchoolName = []
        Ownership = []
        Latitude = []
        Longitude = []

        # Iterating through the json list
        for i in dt['features']:
            Region.append(i['properties']['REGION'])
            Council.append(i['properties']['COUNCIL'])
            Ward.append(i['properties']['WARD'])
            SchoolName.append(i['properties']['SCHOOL_NAM'])
            Ownership.append(i['properties']['OWNERSHIP'])
            Latitude.append(i['properties']['LATITUDE'])
            Longitude.append(i['properties']['LONGITUDE'])

        data = pd.DataFrame.from_dict({'Region': Region,
                            'Council': Council,
                            'Ward': Ward,
                            'SchoolName': SchoolName,
                            'Ownership': Ownership,
                            'Latitude': Latitude,
                            'Longitude': Longitude,})

        print('Data Shape: ', data.shape)
        data.head(10)
        
        data.to_csv('data.csv', index = True)

        # Closing file
        f.close()
        
        data = pd.read_csv('data.csv')
        # data.drop(data.columns[[0]], axis=1, inplace=True)
        # data['Region'] = data['Region'].apply(lambda x: x.title())
        # data['SchoolName'] = data['SchoolName'].apply(lambda x: x.title())
        
        # st.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 5)
        '''
        
        data = pd.read_csv('primary_schools_2019.csv')
        data.drop(data.columns[[0]], axis=1, inplace=True)
        data.drop(data.columns[[10, 11]], axis=1, inplace=True)
        
        data.rename(columns = {'latitude': 'Latitude', 'longitude': 'Longitude', 
                               'altitude': 'Altitude', 'geometry': 'Geometry', 
                               'REGION': 'Region', 'COUNCIL': 'Council', 
                               'WARD': 'Ward', 'SCHOOL_NAM': 'SchoolName',
                               'OWNERSHIP': 'Ownership', 'REGISTRATI': 'Registration', 
                               'TOTAL_POPULATION': 'TotalPopulation'}, inplace = True)
        
        data['Region'] = data['Region'].apply(lambda x: x.title())
        data['SchoolName'] = data['SchoolName'].apply(lambda x: x.title())
        # st.dataframe(data)
        
        st.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 5)
       
    ############################################################################################################
    
    with tab2: 
              
        address = 'Tanzania'

        geolocator = Nominatim(user_agent="four_square")
        location = geolocator.geocode(address) # addressdetails=True
        latitude = location.latitude
        longitude = location.longitude
        # print('The geograpical coordinate of {} are {}, {}.'.format(location, latitude, longitude)) # location.raw # ZipCode: location.address.split(",")[-2]#

        Map = folium.Map(location = [latitude, longitude], zoom_start = 6, tiles="CartoDB positron")
        
        # Add ESRI Satellite Tile Layer
        folium.TileLayer(
            tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            attr='Esri',
            name='Esri Satellite',
            overlay=False,
            control=True
        ).add_to(Map)
        
        Marker = folium.map.FeatureGroup()
        Marker.add_child(folium.CircleMarker([latitude, longitude],
                                                radius = 7,
                                                color = 'red',
                                                # fill_color = 'red',
                                                fill_opacity=0.7))
        Map.add_child(Marker)
        folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = 'home')).add_to(Map) # icon=folium.Icon(color='white', icon = "fa-brands fa-bluesky", icon_color='blue') 
        MousePosition().add_to(Map)
                
        # folium.TileLayer('cartodbdark_matter').add_to(Map)
        # folium_static(Map)
    
        ############################################################################################################
        
        """
        Place = []
        Region = []
        Country = []
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
        
        for i in range(data.shape[0]):

            URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + data['Ward'][i] + ', ' + data['Council'][i] + ', ' + data['Region'][i] + ', Tanzania' + "&aqi=yes"
            response = requests.get(URL) # HTTP request

            dt = response.json()

            Place.append(dt["location"]['name'])
            Region.append(dt['location']['region'])
            Country.append(dt['location']['country'])
            Latitude.append(str(dt['location']['lat']))
            Longitude.append(str(dt['location']['lon']))
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

        status = pd.DataFrame({'Place': Place,
                                'Region': Region,
                                'Country': Country,
                                'SchoolName': data['SchoolName'].values.tolist(),
                                'Ownership': data['Ownership'].values.tolist(),
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

        print('Data Shape: ', status.shape)
        # st.dataframe(status.head(20))
        
        status.to_csv('status.csv', index = True)
        
        status = pd.read_csv('status.csv')
        # st.dataframe(status)
        """
            
        ############################################################################################################
        
        map = st.empty()
        
        st.write('')
        st.write('List of Regions: {}'.format(len(data['Region'].unique())))
        # st.text(data['Region'].unique())
        st.write('Total Schools: {}'.format(len(data['SchoolName'].unique())))
        
        ############################################################################################################
            
        # Adding a sidebar with select boxes
        st.sidebar.header('Select a Location: ')
        region = st.sidebar.selectbox('Select Region', 
                                    tuple(sorted(set(list(data['Region'])))),
                                    index=None,
                                    placeholder="Select Region")

        if region:
            
            st.divider()
            
            st.write('Selected Regions: {}'.format(region))
            st.write('Total Councils: {}'.format(len(data[data['Region'] == region]['Council'].unique())))
            st.write('Total Wards: {}'.format(len(data[data['Region'] == region]['Ward'].unique())))
            st.write('Total Schools: {}'.format(len(data[data['Region'] == region]['SchoolName'].unique())))
                
            """
            map = status.loc[(status['Region'] == region)]
            map.drop(map.columns[[0]], axis=1, inplace=True)
            # st.dataframe(map)
            # st.map(map.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 7)
            """

            map = data.loc[(data['Region'] == region)]
            map = map.reset_index().drop('index', axis = 1)
            # st.dataframe(map)
            
            for idx, row in map.iterrows():
                    folium.Marker([row['Latitude'], 
                                row['Longitude']], 
                                popup = "School Name: " + row['SchoolName'] + ", Ownership Type: " + row['Ownership']).add_to(Map)
                    
            folium_static(Map)
            
            st.divider()
            
            ############################################################################################################
                            
            council = st.sidebar.selectbox('Select Council', 
                                            tuple(sorted(set(list(data.loc[(data['Region'] == region)]['Council'])))),
                                            index=None,
                                            placeholder="Select Council")
                
            if council:   
                        
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
                folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = "home")).add_to(Map)
                MousePosition().add_to(Map)
            
                for idx, row in map.iterrows():
                        folium.Marker([row['Latitude'], 
                                    row['Longitude']], 
                                    popup = "School Name: " + row['SchoolName']).add_to(Map)

                folium_static(Map)
                        
                st.divider()
                
                ############################################################################################################
                               
                ward = st.sidebar.selectbox('Select Ward', 
                                                tuple(sorted(set(list(data.loc[(data['Region'] == region) & (data['Council'] == council)]['Ward'])))),
                                                index=None,
                                                placeholder="Select Ward")
                    
                if ward:   
                                
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
                    folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = "home")).add_to(Map)
                    MousePosition().add_to(Map)
                    
                    for idx, row in map.iterrows():
                            folium.Marker([row['Latitude'], 
                                        row['Longitude']], 
                                        popup = "School Name: " + row['SchoolName']).add_to(Map)

                    folium_static(Map)
                            
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
                        folium.Marker([latitude, longitude], popup = address, icon=folium.Icon(color = 'red', icon = "home")).add_to(Map)
                        MousePosition().add_to(Map)
                        
                        for idx, row in map.iterrows():
                                folium.Marker([row['Latitude'], 
                                            row['Longitude']], 
                                            popup = "School Name: " + row['SchoolName']).add_to(Map)

                        folium_static(Map)
                                
                        st.divider()
                        
                        
    ############################################################################################################                   
    
    with tab3:
        st.write("Weather Analysis")
        
        weather = pd.read_csv('weatherdata.csv')
        st.dataframe(weather)
        
        st.divider()
        
        ##########################################################################################################
                                    
        BASEURL = "http://api.weatherapi.com/v1"
        # st.write("BASE URL: 'http://api.weatherapi.com/v1")
        APIKEY = "6bd51cc56e814b49a4b123504240407" # "316171a92c5d458c85735242213008"
        # st.write("API KEY: ------------------------------")
                        
        Region = []
        Council = []
        Ward = []
        SchoolName = []
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
                                                     
        """
        # URL = "https://api.openweathermap.org/data/2.5/weather?lat={" + latitude + "}&lon={" + longitude + "}&appid={APIKEY}"
        URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + ', ' + region + ', Tanzania' + "&aqi=yes"
                               
        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request
        # if response.status_code == 200:
                                   
        # getting data in the json format
        # data = response.json()
                            
        st.header(f"Location Demographics for {region}")
                            
        P1, P2, P3 = st.columns(3)
        P1.metric(label = "Place",     value = response.json()["location"]['name'])
        P1.metric(label = "Region",    value = response.json()['location']['region'])
        P1.metric(label = "Country",   value = response.json()['location']['country'])
        P2.metric(label = "Latitude",  value = str(response.json()['location']['lat']))
        P2.metric(label = "Longitude", value = str(response.json()['location']['lon']))
        P3.metric(label = "Date",      value = response.json()['location']['localtime'].split()[0])
        P3.metric(label = "Time",      value = response.json()['location']['localtime'].split()[1])
                               
        st.write("")
        st.write("")
        st.write("")
        st.header(f"Concentration of Pollutants in {region}")
                                
        P1, P2, P3, P4, P5, P6 = st.columns(6)
        P1.metric(label = "CO",    value = str(round(response.json()['current']["air_quality"]["co"], 2)))
        P2.metric(label = "NO2",   value = str(round(response.json()['current']["air_quality"]["no2"], 2)))
        P3.metric(label = "O3",    value = str(round(response.json()['current']["air_quality"]["o3"], 2)))
        P4.metric(label = "SO2",   value = str(round(response.json()['current']["air_quality"]["so2"], 2)))
        P5.metric(label = "PM2.5", value = str(round(response.json()['current']["air_quality"]["pm2_5"], 2)))
        P6.metric(label = "PM10",  value = str(round(response.json()['current']["air_quality"]["pm10"], 2)))
                                
        st.write("")
        st.write("")
        st.write("")
        st.header(f"Weather Attributes for {region}")
                                        
        P1, P2, P3, P4, P5, P6, P7 = st.columns(7)
        P1.metric(label = "Wind Speed (mph): ",  value = str(response.json()['current']["wind_mph"]))
        P1.metric(label = "Wind Degree: ",       value = str(response.json()['current']["wind_degree"]))
        P1.metric(label = "Wind Direction: ",    value = response.json()['current']["wind_dir"])
                                
        P2.metric(label = "Gust (mph): ",  value = str(response.json()['current']["gust_mph"])) 
                               
        P3.metric(label = "Pressure (ml): ",  value = str(response.json()['current']["pressure_mb"]))
                                
        P4.metric(label = "Precipation (mm): ",    value = str(response.json()['current']["precip_mm"]))      
                                
        P5.metric(label = "Temperature (C): ",  value = str(response.json()['current']["feelslike_c"])) 
                              
        P6.metric(label = "Visibility (miles): ",  value = str(response.json()['current']["vis_miles"]))
                              
        P7.metric(label = "Humidity: ",  value = str(response.json()['current']["humidity"]))
        P7.metric(label = "Cloud: ",     value = str(response.json()['current']["cloud"]))
        P7.metric(label = "UV: ",        value = str(response.json()['current']["uv"]))
        """
                        
        """
        hm = HeatMap(list(zip(status.Latitude.values, status.Longitude.values, status.Temperature.values)),
                         min_opacity=0.2,
                         max_val = float(status.Temperature.max()),
                         radius=17, 
                         blur=15,
                         max_zoom=1 
                        )
        """
                        
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
        folium_static(Map)      
                       
        ######################################################################################################
        