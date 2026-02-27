import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


def home():
    # page config
    st.set_page_config(
        page_title="Home Page: Medical Cost Predictor · Nigeria",
        page_icon="🏥",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    
    hide_default_sidebar = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
    """
    st.markdown(hide_default_sidebar, unsafe_allow_html=True)


    # header
    st.title("🏥 Medical Cost Prediction System")
    st.caption("")
    st.markdown("---")
    
    # navigations
    with st.sidebar:
        st.markdown("### 🏥 MediCost NG")
        st.markdown("---")
        st.markdown("**Navigation**")
        st.page_link("home.py",                label="🏠 Home",               )
        st.page_link("pages/eda_dashboard.py",           label="📊 EDA Dashboard",      )
        st.page_link("pages/medical_cost_predictor.py",    label="🔮 Medical Cost Predictor",       )
        st.page_link("pages/prediction_result.py",       label="📋 Prediction Results", )
        st.markdown("---")
        st.markdown("**Project Info**")
        st.markdown("Dataset: `nigeria_medical_insurance.csv`")
        st.markdown("Model: Regression ensemble")
        st.markdown("Version: 1.0.0")
        
        

    # about and business context
    col_a, col_b = st.columns([3, 2], gap="large")
    with col_a:
        st.markdown("""
            About the Project
            
            ### Why This System Matters
            
            Healthcare costs in Nigeria vary dramatically across lifestyle factors, geography, and demographics.
            Insurance companies currently rely on manual judgement or overly broad actuarial tables that
            introduce pricing bias and underwriting risk.
            
            This project delivers a strong data-driven ***Medical Cost Prediction System***, trained on 
            real Nigerian insurance records, that replaces guesswork with statistically sound estimates.
            The system processes patient attributes such as age, BMI, smoking status, number of dependants,
            and state to predict expected medical charges with measurable accuracy.
        """)

    with col_b:
        st.markdown("""
            Business Questions Answered
            
            ### What We Solve
            
            💰 ***Accurate bill estimation*** Predict individual hospital charges before underwriting a policy.
            
            ⚠️ ***High-risk patient flags*** Identify cost-heavy profiles early to adjust premium tiers.
            
            ⚖️ ***Reduce underwriting bias*** Replace subjective pricing with model-driven, auditable scores.
            
            🔍 ***Pricing transparency*** Give customers a clear rationale for the premium they pay.
        """)

    st.markdown("---")
    st.markdown("""
        Methodology
        
        ### Project Objectives
    """)

    obj_cols = st.columns(4, gap="medium")
    with obj_cols[0]:
        st.markdown("""
            🧹
            
            **Data Cleaning**
            
            Handle missing values and inconsistencies, standardise column and remove noise from the raw CSV.
        """)
    with obj_cols[1]:
        st.markdown("""
            📊
            
            **Exploratory Analysis**
            
            Profile distributions, detect outliers, analyse correlations, and surface patterns that drive medical costs.
        """)
    with obj_cols[2]:
        st.markdown("""
            🤖
            
            **Model Building**
            
            Train and compare multiple regression models; Linear, Ridge, Random Forest, XGBoost, on cleaned data.
        """)
    with obj_cols[3]:
        st.markdown("""
            📋
            
            **Business Insights**
            
            Translate model outputs into actionable recommendations for pricing teams and risk analysts.
        """)
        
    st.markdown("---")
    
           
    st.markdown("""
        Navigation
        
        ### What's Inside This Dashboard
        
        The dashboard is split into three focused pages. Use the sidebar or the cards below to explore each section.
    
    """)

    p1, p2, p3 = st.columns(3, gap="medium")
    with p1:
        st.markdown("""
            📊 **EDA Dashboard**
            
            Interactive visualisations of the cleaned dataset; distributions, correlations, and cost breakdowns across all features
        """)
        if st.button("📊  EDA Dashboard", use_container_width=True):
            with st.spinner("EDA Dashboard Page Loading..."):
                st.switch_page("pages/eda_dashboard.py")
                
    with p2:
        st.markdown("""
            🔮 **Medical Cost Predictor**
            
            Input patient attributes via a form and receive an instant medical cost estimate powered by the best-performing model.
        """)
        if st.button("🔮  Medical Cost Predictor", use_container_width=True):
            with st.spinner("Medical Cost Predictor Page Loading..."):
                st.switch_page("pages/medical_cost_predictor.py")
                
    with p3:
        st.markdown("""
            📋 **Model Evaluation**
            
            Inspect model performance metrics (R², RMSE, MAE), and download for report.
        """)
        if st.button("📋  Model Evaluation", use_container_width=True):
            with st.spinner("Model Evaluation Metrics Page Loading..."):
                st.switch_page("pages/model_eval.py")
        
    st.markdown("---")


home()