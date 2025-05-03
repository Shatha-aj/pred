import streamlit as st
import pandas as pd
import joblib

# Load model and helpers

import os

model = joblib.load("accident_model.pkl")
label_encoder = joblib.load("label_encoder.pkl")
columns = joblib.load("columns.pkl")

st.set_page_config(page_title="Accident Severity Predictor", layout="centered")
st.markdown("""
    <style>
    html, body, .stApp {
        background: linear-gradient(120deg, #e0f7fa, #fce4ec);
        font-family: 'Segoe UI', sans-serif;
    }

    .stApp {
        padding: 20px;
    }

    .stTitle {
        color: #2c3e50;
        text-align: center;
        margin-bottom: 1em;
    }

    .stSelectbox > label {
        font-weight: 600;
        color: #37474f;
    }
    /* Style for selectbox labels */
label {
    color: #1a237e !important;
    font-weight: bold !important;
    font-size: 1rem !important;
}


    .stButton > button {
        background: linear-gradient(to right, #42a5f5, #7e57c2);
        color: white;
        font-weight: bold;
        border-radius: 30px;
        padding: 0.6em 2em;
        border: none;
        transition: 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(to right, #7e57c2, #42a5f5);
        transform: scale(1.05);
    }

    .result-box {
        background-color: #ffffffdd;
        border-left: 6px solid #7e57c2;
        padding: 1rem;
        border-radius: 10px;
        font-size: 1.2rem;
        color: #2c3e50;
        margin-top: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
    }

    .stForm {
        background-color: rgba(255,255,255,0.85);
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 0 10px rgba(0,0,0,0.05);
        margin-top: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

  


    

  


st.title("🚦 Accident Severity Prediction")
st.markdown("Use this app to predict the likely severity of a road accident based on driving and environmental conditions.")

# Input fields
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
       sex = st.selectbox("🚻 Sex of Driver", ["Male", "Female"])
       age_band = st.selectbox("👤 Age Band of Driver", ["18-30", "31-50", "Over 51", "Under 18"])
       experience = st.selectbox("Driving Experience", ["1-2yr", "2-5yr", "5-10yr", "Above 10yr", "below 1yr"])
    with col2:
        day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        road = st.selectbox("Road Surface Conditions", ["Dry", "Wet or damp", "Snow", "Flood over 3cm. deep"])
        light = st.selectbox("Light Conditions", ["Darkness - no lighting", "Daylight", " Darkness - lights unlit","Darkness - lights lit"])
        weather = st.selectbox("Weather Conditions", ["Normal", "Raining", "Cloudy"])

    submitted = st.form_submit_button("Predict Severity")

if submitted:
    # Prepare input DataFrame
    input_dict = {
        "Day_of_week": [day],
        "Age_band_of_driver": [age_band],
        "Sex_of_driver": [sex],
        "Driving_experience": [experience],
        "Road_surface_conditions": [road],
        "Light_conditions": [light],
        "Weather_conditions": [weather]
    }

    input_df = pd.DataFrame(input_dict)
    input_df = pd.get_dummies(input_df)

    # Add missing columns and reorder
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=columns, fill_value=0)

    # Predict
    prediction = model.predict(input_df)
    severity = label_encoder.inverse_transform(prediction)

    st.success(f"🚨 Predicted Accident Severity: {severity[0]}")
