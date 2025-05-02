import streamlit as st
import pandas as pd
import joblib

# Load model and helpers

import os

model_path = os.path.join(os.getcwd(), 'accident_model.pkl')
model = joblib.load(model_path)

st.set_page_config(page_title="Accident Severity Predictor", layout="centered")

st.markdown("""
    <style>
    .main {
        background: linear-gradient(to bottom right, #e0f7fa, #ffffff);
        padding: 20px;
        border-radius: 12px;
    }

    .stApp {
        background-color: #fdfdfd;
    }

    .stButton>button {
        background-color: #2196F3;
        color: white;
        font-weight: 600;
        border: none;
        border-radius: 8px;
        padding: 0.6em 1.5em;
        transition: 0.3s;
    }

    .stButton>button:hover {
        background-color: #1976D2;
    }

    .block-container {
        padding-top: 2rem;
    }

    .result-box {
        padding: 1.2em;
        border-radius: 10px;
        text-align: center;
        font-size: 1.3em;
        font-weight: bold;
    }

    .mild {
        background-color: #c8e6c9;
        color: #256029;
    }

    .serious {
        background-color: #ffe082;
        color: #795548;
    }

    .fatal {
        background-color: #ef9a9a;
        color: #b71c1c;
    }
    </style>
""", unsafe_allow_html=True)


st.title("🚦 Accident Severity Prediction")
st.markdown("Use this app to predict the likely severity of a road accident based on driving and environmental conditions.")

# Input fields
with st.form("input_form"):
    col1, col2 = st.columns(2)
    with col1:
        time = st.selectbox("Time of Day", ["Morning", "Afternoon", "Evening", "Night"])
        sex = st.selectbox("Sex of Driver", ["Male", "Female"])
        age_band = st.selectbox("Age Band of Driver", ["18-30", "31-50", "Over 51", "Under 18"])
        experience = st.selectbox("Driving Experience", ["1-2yr", "2-5yr", "5-10yr", "Above 10yr", "below 1yr"])
    with col2:
        day = st.selectbox("Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"])
        road = st.selectbox("Road Surface Conditions", ["Dry", "Wet", "Snow", "Flood"])
        light = st.selectbox("Light Conditions", ["No lighting", "Day lighting", "lights unlit","lights lit"])
        weather = st.selectbox("Weather Conditions", ["Normal", "Raining", "cloudy"])

    submitted = st.form_submit_button("Predict Severity")

if submitted:
    # Prepare input DataFrame
    input_dict = {
        "Time": [time],
        "Day_of_week": [day],
        "Age_band_of_driver": [age_band],
        "Sex_of_driver": [sex],
        "Driving_experience": [experience],
        "Type_of_vehicle": [vehicle],
        "Area_accident_occured": [area],
        "Road_surface_conditions": [road],
        "Light_conditions": [light],
        "Weather_conditions": [weather],
        "Cause_of_accident": [cause],
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
