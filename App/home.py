# RESOURCES
# https://docs.streamlit.io/develop/api-reference

# VERSION 1

# Foursquare
# 1. https://docs.foursquare.com/developer/reference/address-directory
# 2. https://docs.foursquare.com/developer/reference/address-form-autofill
# 3. https://docs.foursquare.com/developer/reference/local-search-map

# Folium
# 1. https://folium.streamlit.app/
# 2. https://realpython.com/python-folium-web-maps-from-data/

# Stremlit Pills
# 1. https://pypi.org/project/streamlit-pills/
# 2. https://discuss.streamlit.io/t/how-to-add-a-title-text-or-few-sample-prompts-close-to-the-chat-input/64757

# Standardize Text
# 1. https://pypi.org/project/Unidecode/
# 2. https://pypi.org/project/anyascii/0.1.6/

#--------------------------------------------------------------------------------------------------------------

# VERSION 2:

# Streamlit Range Slider
# https://docs.streamlit.io/develop/api-reference/widgets/st.slider

# Gradient Animation
# https://lottiefiles.com/animations/gradient-loader-02-juQh1tTYA0
# https://lottie.host/ca52053c-bcc2-423b-9258-1e2ebe84aa4f/vE2uf9LsAY.json
# https://lottie.host/f34a0bc0-4b98-4632-8684-4fbfadf0806f/8qPOuRLkVc.json
# https://lottie.host/bfc80cbd-79f1-4d62-ad2d-89f4e9f3278d/Z1fopF3tEc.json

# Select Box
# https://docs.streamlit.io/develop/api-reference/widgets/st.selectbox

# Toast
# https://docs.streamlit.io/develop/api-reference/status/st.toast
# https://fonts.google.com/icons?icon.set=Material+Symbols&icon.style=Outlined

# Geolocation
# https://pypi.org/project/streamlit-geolocation/

# Divider
# https://docs.streamlit.io/develop/api-reference/text/st.divider

# Infomation Message
# https://docs.streamlit.io/develop/api-reference/status/st.info

###############################################################################################################

# LIBRARIES

import streamlit as st # Version 1
# st.set_page_config(layout="wide")
from streamlit_lottie import st_lottie # Version 2

import requests # library to handle requests # Version 1
import numpy as np # library to handle data in a vectorized manner # Version 1
import random # library for random number generation # Version 1

# !conda install -c conda-forge geopy --yes
from geopy.geocoders import Nominatim # module to convert an address into latitude and longitude values # Version 1
import geocoder

import json # library to handle JSON files

# from pandas.io.json import json_normalize
from pandas import json_normalize # tranform JSON file into a pandas dataframe # Version 1

# !conda install -c conda-forge folium=0.5.0 --yes
import folium # plotting library # Version 1
# from streamlit_folium import st_folium # type: ignore

import pandas as pd # library for data analsysis
pd.set_option('display.max_columns', None) # Version 1
pd.set_option('display.max_rows', None) # Version 1

import time # Version 2

import geopandas as gpd
import folium
from folium.plugins import HeatMap

print('Libraries Imported')

###############################################################################################################

st.toast('Welcome to Omdena OpenDevEd!!!', icon='🎉')

###############################################################################################################

# @st.cache_data(experimental_allow_widgets=True)
def app():
    
    ###########################################################################################################
    
    st.write("")
        
    st.title("Omdena OpenDevEd")
    
    st.write("")
    
    st.header("Gelocation of Schools in Tanzania")
    
    st.write("")
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
    '''
    
    data = pd.read_csv('data.csv')
    
    st.map(data.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 5)
       
    ############################################################################################################
    
    address = 'Mwanza, Mwanza, Tanzania'

    geolocator = Nominatim(user_agent="four_square")
    location = geolocator.geocode(address) # addressdetails=True
    latitude = location.latitude
    longitude = location.longitude
    # print('The geograpical coordinate of {} are {}, {}.'.format(location, latitude, longitude)) # location.raw # ZipCode: location.address.split(",")[-2]#

    '''
    Map = folium.Map(location = [latitude, longitude], zoom_start = 6)

    Marker = folium.map.FeatureGroup()
    Marker.add_child(folium.CircleMarker([latitude, longitude],
                                                radius = 5,
                                                color = 'red',
                                                fill_color = 'Red'))
    Map.add_child(Marker)
    folium.Marker([latitude, longitude], popup = address).add_to(Map)

    st.pydeck_chart(Map)
    '''
    
    ############################################################################################################
    
    """
    for i in range(data.shape[0]):

        '''
        geolocator = Nominatim(user_agent="four_square")
        location = geolocator.geocode(df.City[i] + ', ' + status.Region[i] + ', Tanzania')
        latitude = location.latitude
        longitude = location.longitude
        # print('{}: The geograpical coordinate of {} are {}, {}.'.format(i+1, location, latitude, longitude)) # location.raw
        '''

        Marker.add_child(folium.CircleMarker([data['Latitude'][i], data['Longitude'][i]],
                                                    radius = 5,
                                                    color = 'blue',
                                                    fill_color = 'blue'))
        Map.add_child(Marker)
        folium.Marker([latitude, longitude], popup = data['SchoolName'][i]).add_to(Map)

    # st.plotly_chart(Map)
    """
    
    ############################################################################################################
    
    BASEURL = "http://api.weatherapi.com/v1"
    #st.write("BASE URL: 'http://api.weatherapi.com/v1")
    APIKEY = "316171a92c5d458c85735242213008"
    #st.write("API KEY: ------------------------------")
    
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
    """
    
    status = pd.read_csv('status.csv')
    
    ############################################################################################################
    
    st.write('*List of Regions:')
    st.text(sorted(status['Region'].unique()))
    # st.write('\nList of Councils')
    # st.text(sorted(data['Council'].unique()))
    # st.write('\nList Wards:')
    # st.text(sorted(data['Ward'].unique()))
    
    ############################################################################################################
    
    map = st.empty()
    
    # Adding a sidebar with select boxes
    st.sidebar.header('Select a Location: ')
    region = st.sidebar.selectbox('Select Region', 
                                  tuple(sorted(set(list(status['Region'])))),
                                  index=None,
                                  placeholder="Select Region")

    if region:
        map = status.loc[(status['Region'] == region)]
        # st.dataframe(map)
        st.map(map.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 7)
            
        ############################################################################################################
         
        """    
        place = st.sidebar.selectbox('Select Place', 
                                     tuple(sorted(set(list(status[status['Region'] == region]['Place'])))),
                                     index=None,
                                     placeholder="Select Place")
        
        if place:   
            # map = status.loc[(status['Region'] == region) & (status['Place'] == place)]
            # st.dataframe(map)            
            # st.map(map.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 12)
            
            ############################################################################################################
            
            ownership = st.sidebar.selectbox('Select Ownership', 
                                        tuple(sorted(set(list(status.loc[(status['Region'] == region) & (status['Place'] == place)]['Ownership'])))),
                                        index=None,
                                        placeholder="Select Ownership")
            
            if ownership:   
                map = status.loc[(status['Region'] == region) & (status['Place'] == place) & (status['Ownership'] == ownership)]
                map.drop(map.columns[[0]], axis=1, inplace=True)
                # st.dataframe(map)            
                st.map(map.rename(columns = {'Latitude': 'latitude', 'Longitude': 'longitude'}), zoom = 12)
                """
                
                             
        URL = BASEURL + "/current.json?key=" + APIKEY + "&q=" + ', ' + region + ', Tanzania' + "&aqi=yes"
                
        # HTTP request
        response = requests.get(URL)
        # checking the status code of the request
        # if response.status_code == 200:
                    
        # getting data in the json format
        data = response.json()
                
        """ 
        st.header(f"Location Demographics for {region}")
               
        P1, P2, P3 = st.columns(3)
        P1.metric(label = "Place",     value = response.json()["location"]['name'])
        P1.metric(label = "Region",    value = response.json()['location']['region'])
        P1.metric(label = "Country",   value = response.json()['location']['country'])
        P2.metric(label = "Latitude",  value = str(response.json()['location']['lat']))
        P2.metric(label = "Longitude", value = str(response.json()['location']['lon']))
        P3.metric(label = "Date",      value = response.json()['location']['localtime'].split()[0])
        P3.metric(label = "Time",      value = response.json()['location']['localtime'].split()[1])
        """
                
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
                        
                
