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
    
    # navigations
    hide_default_sidebar = """
    <style>
        [data-testid="stSidebarNav"] {display: none;}
    </style>
        """
    st.markdown(hide_default_sidebar, unsafe_allow_html=True)

    with st.sidebar:
        st.markdown("### 🏥 MediCost NG")
        st.markdown("---")
        st.markdown("**Navigation**")
        st.page_link("home.py",                label="🏠 Home",               )
        st.page_link("pages/eda_dashboard.py",           label="📊 EDA Dashboard",      )
        st.page_link("pages/medical_cost_predictor.py",    label="🔮 Medical Cost Predictor",       )
        st.page_link("pages/model_eval.py",       label="⚖️ Model Evaluation", )
        st.markdown("---")
        st.markdown("**Project Info**")
        st.markdown("Dataset: `nigeria_medical_insurance.csv`")
        st.markdown("Model: Regression ensemble")
        st.markdown("Version: 1.0.0") 
        
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
        smoker_percentage = percentage_smoker[0]
        
    else:
        avg_hospital_bill = 0
        avg_age = 0
        avg_bmi = 0
        smoker_percentage = 0.00
    
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
            f"{smoker_percentage:.1f}%",
            color="#9b59b6"
        )
        
        
    # row 1 - hospital bill distribution and smoker vs non-smoker
    left, right = st.columns(2)
    with left:
        st.subheader("Hospital Bill Distribution")
        fig_hospital_bill = px.histogram(
            filtered_df,
            x="hospital_bill",
            title="Distribution of Hospital Bills"
        )
        st.plotly_chart(fig_hospital_bill, use_container_width=True)
        fig_hospital_bill.update_layout(showlegend=False)
    
        
    with right:
        st.subheader("Patient Age Distribution")
        fig_age = px.histogram(
            filtered_df,
            x="age",
            title="Distribution of Age"
        )
        st.plotly_chart(fig_age, use_container_width=True)
        fig_age.update_layout(showlegend=False)
    
        
        
        
    st.markdown("---") 
     
     
    # row 2 - average hospital bill by smoker status and average hospital bill by state
    left, right = st.columns(2)
    with left:
        st.subheader("Smoker vs Non-Smoker Distribution")   
        fig_smoker_distribution = px.pie(
            filtered_df,
            names="smoker",
            title="Distribution of Smoker vs Non-Smoker",
            color_discrete_sequence=px.colors.qualitative.Set2,
            hole=0.4 
        )
        st.plotly_chart(fig_smoker_distribution, use_container_width=True)
        fig_smoker_distribution.update_layout(showlegend=False)
        
        
    with right:
        smooker_bill = filtered_df.groupby("smoker")["hospital_bill"].mean().reset_index()
        st.subheader("Average Hospital Bill by Smoker Status")
        fig_bar = px.bar(
            smooker_bill,
            x="hospital_bill",
            y="smoker",
            orientation="h", 
            title="Average Hospital Bill by Smoker Status",
            labels={"smoker": "Smoker Status", "hospital_bill": "Average Hospital Bill (₦)"}
        )
        st.plotly_chart(fig_bar, use_container_width=True)
        
        st.markdown("---")
        
        
    # row 3 - average hospital bill by state and correlation matrix
    left, right = st.columns(2)
    with left:
        st.subheader("Average Hospital Bill by State")
        state_bill = filtered_df.groupby("state")["hospital_bill"].mean().reset_index()
        fig_state_bar = px.bar(
            state_bill,
            x="state",
            y="hospital_bill",
            title="Average Hospital Bill by State",
            labels={"state": "State", "hospital_bill": "Average Hospital Bill (₦)"},
            color="hospital_bill",
            color_continuous_scale=px.colors.sequential.Reds
        )
        st.plotly_chart(fig_state_bar, use_container_width=True)
        
    with right:
        st.subheader("Correlation Matrix")
        corr_matrix = filtered_df.select_dtypes(include=['float64', 'int64']).corr()
        fig_corr = px.imshow(
            corr_matrix, 
            title="Correlation Matrix"
        )
        st.plotly_chart(fig_corr, use_container_width=True)
        
    st.markdown("---")
    
        
    # data overview
    st.subheader("Data Preview")
    st.dataframe(filtered_df.head())
    
    # prediction system
    st.markdown("---") 
    if st.button("Predict Your Medical Bill here", type="primary", use_container_width=True):
        with st.spinner("Page loading..."):
            st.switch_page("pages/medical_cost_predictor.py")
    
    
    
    # footer
    st.markdown("---")
    st.caption("Customer churn prediction system")
    
medical_bill_dashboard()