import pandas as pd
import folium
import streamlit as st
import pickle
from folium.plugins import Draw
import os
from streamlit_folium import st_folium
from borogh import get_patrol_borough
def custom_warning(message):
    st.markdown(
        f"""
        <div id="custom-warning" style='background-color:red; padding:10px;border-radius:5px;'>
            <p style='color:white;font-size:18px;font-weight:bold;'>Warning: {message}</p>
        </div>
        <style>
            @keyframes blink {{
                0%, 50%, 100% {{
                    background-color: red;
                }}
                25%, 75% {{
                    background-color: transparent;
                }}
            }}
            #custom-warning {{
                animation: blink 2s;
            }}
        </style>
        """,
        unsafe_allow_html=True
    )
def predict(data):
    with open('../model/random_forest_model.pkl', 'rb') as file:
        loaded_model = pickle.load(file)


    # Perform prediction on the example data point
    prediction = loaded_model.predict(data)
    return prediction[0]
    #print(f'Predicted class for the example data point: {prediction[0]}')

def main():
    col1, col2 = st.columns([4, 1])
    with col1:
        st.subheader("Map :")
        m = folium.Map(location=[40.730610, -73.935242], zoom_start=10)
        draw_options = {"polyline": False, "rectangle": False, "circle": False, "circlemarker": False, "marker": True,
                        "polygon": False}
        Draw(export=False,draw_options=draw_options).add_to(m)
        def on_marker_click(e):
            if e["last_active_drawing"] is not None:
                coordinates = e["last_active_drawing"]["geometry"]["coordinates"]
                lat, lng = coordinates[1], coordinates[0]
                nearest_patrol_borough = get_patrol_borough(lat, lng)
                return nearest_patrol_borough, lat, lng
            else:
                return None, None, None
        output = st_folium(m, width=700, height=500)
        nearest_patrol_borough,lat,lng = on_marker_click(output)


    with col2:
        st.sidebar.subheader("Enter your  data")

        gender = st.sidebar.radio(
            " What\'s your gender",
            ('Male', 'Female', 'Other'))
        date = st.sidebar.date_input("pick a date", value=None, min_value=None, max_value=None, key=None)
        P_age = st.sidebar.slider('Pick an age', 0, 100, 24)
        if P_age <=18:
            age = '<18'
        elif P_age >18 and P_age <=24:
            age = '18-24'
        elif P_age >24 and P_age <=44:
            age = '25-44'
        elif P_age >44 and P_age <=64:
            age = '45-64'
        elif P_age >64:
            age = '65+'
        else:
            age = 'UNKNOWN'


        race = st.sidebar.selectbox(
            'Pick your race ',
            ('WHITE','BLACK', 'ASIAN','UNKNOWN'))

        #place = st.sidebar.radio("Place:", ('BROOKLYN', 'STATEN ISLAND', 'BRONX', 'QUEENS', 'MANHATTAN', 'UNKNOWS'))
        place_type = st.sidebar.selectbox( 'Pick your destination type ',('CHAIN STORE','COMMERCIAL BUILDING','GROCERY/BODEGA',
                                                                          'OTHER','RESIDENCE - APT. HOUSE','RESIDENCE - PUBLIC HOUSING',
                                                                          'RESIDENCE-HOUSE','STREET','TRANSIT - NYC SUBWAY'))
        



#_____________Model part______________________
        
    # borough_mapping = {
    # 'PATROL BORO BKLYN NORTH': 'BROOKLYN',
    # 'PATROL BORO BRONX': 'BRONX',
    # 'PATROL BORO MAN SOUTH': 'MANHATTAN',
    # 'PATROL BORO BKLYN SOUTH': 'BROOKLYN',
    # 'PATROL BORO QUEENS SOUTH': 'QUEENS',
    # 'PATROL BORO QUEENS NORTH': 'QUEENS',
    # 'PATROL BORO MAN NORTH': 'MANHATTAN',
    # 'PATROL BORO STATEN ISLAND': 'STATEN ISLAND'}
                
    model_day = None
    model_month = None
    model_gender = None
    model_boro = None
    model_prem = None
    model_age = None
    model_race = None

    race_mapping = {
        'WHITE': 2,
        'BLACK': 0,
        'UNKNOWN': 1,
        'ASIAN': 3,
    }
    
    age_mapping = {
        '18-24': 0,
        '25-44': 1,
        '45-64': 2,
        '65+': 3,
        '<18': 4,
        'UNKNOWN': 5
    }
    gender_mapping = {
        'Male': 1,
        'Female': 0,
        'Other': 2
    }
    patrol_borough_mapping = {
    'PATROL BORO BKLYN NORTH': 0,
    'PATROL BORO BKLYN SOUTH': 1,
    'PATROL BORO BRONX': 2,
    'PATROL BORO MAN NORTH': 3,
    'PATROL BORO MAN SOUTH': 4,
    'PATROL BORO QUEENS NORTH': 5,
    'PATROL BORO QUEENS SOUTH': 6,
    'PATROL BORO STATEN ISLAND': 7,
    None: 8  }

    location_type_mapping = {
    'CHAIN STORE': 0,
    'COMMERCIAL BUILDING': 1,
    'DEPARTMENT STORE': 2,
    'GROCERY/BODEGA': 3,
    'OTHER': 4,
    'RESIDENCE - APT. HOUSE': 5,
    'RESIDENCE - PUBLIC HOUSING': 6,
    'RESIDENCE-HOUSE': 7,
    'STREET': 8,
    'TRANSIT - NYC SUBWAY': 9
}

    model_day = date.day
    model_month = date.month

    if gender in gender_mapping:
        model_gender = gender_mapping[gender]

    if nearest_patrol_borough in patrol_borough_mapping:
        model_boro = patrol_borough_mapping[nearest_patrol_borough]

    if place_type in location_type_mapping:
        model_prem = location_type_mapping[place_type]

    if age in age_mapping:
        model_age = age_mapping[age]

    if race in race_mapping:
        model_race = race_mapping[race]

    # Create the details dictionary
    details = {'day': model_day, 'month': model_month,'PREMISES_GROUP': model_prem,'PATROL_BORO': model_boro, 
            'Latitude': lat, 'Longitude': lng, 'VIC_RACE_GROUPED': model_race,'Gender': model_gender, 'VIC_AGE_GROUP': model_age}
    print(details)

    with col1:
        if st.button("Predict"):
            if output["last_active_drawing"] is not None:
                with st.spinner("Predicting..."):
                    df = pd.DataFrame(details, index=[0])
                    prediction = predict(df)
                    custom_warning(f"High likelihood of a {prediction}")
            else:
                st.warning("Please click on the map marker to provide location data before predicting.")

if __name__ == "__main__":
    main()
