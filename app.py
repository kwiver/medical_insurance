import streamlit as st
import numpy as np
import pandas as pd
import joblib

# page config
st.set_page_config(
    page_title="Medical Bill Prediction System",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
    <style>
        .main-title {
            font-size: 40px;
            font-weight: bold;
            color: #2E86C1;
        }
        .sub-text {
            font-size:18px;
            color: gray;
        }
        .prediction-card {
            padding: 25px;
            border-radius: 15px;
            background-color: #F4F6F7;
            box-shadow: 0px 4px 10px rgba(0,0,0,0.1);
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    # model = joblib.load("medical_model.pkl")
    model = None
    return model
model = load_model()

st.markdown('<p class="main-title">🏥 Medical Bill Prediction Dashboard</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">Predict estimated hospital/medical bills using patient information.</p>', unsafe_allow_html=True)

st.divider()