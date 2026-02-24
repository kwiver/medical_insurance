# import libraries
import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

def medical_bill_dashboard():
    # page config
    st.set_page_config(
        page_title="Medical Insurance Dashboard",
        layout="wide",
        initial_sidebar_state="expanded"
    )  
        
    #load datast
    df = pd.read_csv("../data/cleaned/cleaned_nigeria_medical_insurance.csv")
    
    # header
    st.title("🏥 Medical Insurance Dashboard")
    st.caption("A strategic overview of medical insurance data")
    st.markdown("---")
    
     # Sidebar Title
    st.sidebar.markdown("## 🧭 Dashboard Filters")
    st.sidebar.markdown("Fine-tune the dashboard using the filters below.")
    
     # age filter
    age_filter = st.sidebar.multiselect(
        "Age",
        options=sorted(df["age"].unique().tolist()),
        default=sorted(df["age"].unique().tolist())
    )
    
    # bmi filter
    min_bmi = float(df["bmi"].min())
    max_bmi = float(df["bmi"].max())

    bmi_range = st.sidebar.slider(
        "Select BMI Range",
        min_value=min_bmi,
        max_value=max_bmi,
        value=(min_bmi, max_bmi)
    )
    
     # smoker filter
    smoker_filter = st.sidebar.multiselect(
        "Smoker",
        options=df["smoker"].unique(),
        default=df["smoker"].unique()
    )
    
     # state filter
    state_filter = st.sidebar.multiselect(
        "State",
        options=df["state"].unique(),
        default=df["state"].unique()
    )
    
     # apply filter
    filtered_df = df[
        (df["age"].isin(age_filter)) &
        (df["bmi"] >= bmi_range[0]) &
        (df["bmi"] <= bmi_range[1]) &
        (df["smoker"].isin(smoker_filter)) &
        (df["state"].isin(state_filter))
    ]
    
    def kpi_card(title, value, icon="📊", color="#2E86C1"):
        st.markdown(
            f"""
            <div style="
                background-color: white;
                padding: 20px;
                border-radius: 15px;
                box-shadow: 2px 4px 12px rgba(0,0,0,0.08);
                text-align: center;
                border-left: 6px solid {color};
            ">
                <div style="font-size:20px; color:gray;">{title}</div>
                <div style="font-size:24px; font-weight:bold; margin-top:5px;">
                    {value}
                </div>
            </div>
            """,
            unsafe_allow_html=True
    )
    

    # kpi summary
    if not filtered_df.empty:
        avg_hospital_bill = filtered_df["hospital_bill"].mean()
        avg_age = filtered_df["age"].mean()
        avg_bmi = filtered_df["bmi"].mean()
        percentage_smoker = (filtered_df["smoker"].value_counts(normalize=True) * 100)
        
    else:
        total_revenue = 0
        total_rental = 0
        active_customers = 0
        monthly_growth = 0
        

    
    # display KPIs
    # col1, col2, col3, col4 = st.columns(4)
    # with col1:
    #     st.metric("Average Hospital Bill", f"₦{avg_hospital_bill:,.2f}")
    # with col2:
    #     st.metric("Average Age", f"{avg_age:.0f}")
    # with col3:
    #     st.metric("Average BMI", f"{avg_bmi:.2f} kg/m²")
    # with col4:
    #     st.metric("Percentage Smoker", f"{percentage_smoker.iloc[0]:.1f}%")
    
    
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        kpi_card(
            "💰Average Hospital Bill",
            f"₦{avg_hospital_bill:,.2f}",
            color="#3498db"
        )

    with col2:
        kpi_card(
            "👴Average Age",
            f"{avg_age:.0f} years",
            color="#27ae60"
        )

    with col3:
        kpi_card(
            "📊Average BMI",
            f"{avg_bmi:.2f} kg/m²",
            color="#e74c3c"
        )
    
    with col4:
        kpi_card(
            "🚬Percentage Smoker",
            f"{percentage_smoker.iloc[1]:.1f}%",
            color="#9b59b6"
        )

medical_bill_dashboard()