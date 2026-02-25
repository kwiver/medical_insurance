import streamlit as st

st.set_page_config(
    page_title = "Prediction Result",
    page_icon = "📄",
    layout = "centered",
    initial_sidebar_state = "expanded"
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
    st.page_link("pages/prediction_result.py",       label="📋 Prediction Results", )
    st.markdown("---")
    st.markdown("**Project Info**")
    st.markdown("Dataset: `nigeria_medical_insurance.csv`")
    st.markdown("Model: Regression ensemble")
    st.markdown("Version: 1.0.0")

st.title("📄 Prediction Result")
if "predicted_bill" not in st.session_state:
    st.warning("No prediction found. Please make a prediction first.")
    st.stop()

result = st.session_state.predicted_bill
risk = st.session_state.calculate_risk
age = st.session_state.age
bmi = st.session_state.bmi
smoker = st.session_state.smoker
gender = st.session_state.gender
state = st.session_state.state
children = st.session_state.children

st.markdown("---")
# predicted bill
st.subheader(
    f"Estimated medical bill : ₦{result:,.2f}"
)
# risk_level
if risk["risk_level"] == "High":
    st.warning(f"### ⚠️ Risk Level: {risk['risk_level']} | Risk color: {risk['risk_color']}⚠️.")
else:
    st.success(f"### ✅ Risk Level: {risk['risk_level']} | Risk color: {risk['risk_color']}✅.")

# interpretation
st.markdown("---")
st.subheader("🔍 Interpretation")
                    
if risk["risk_level"] == "High":
    st.warning("""
         
    """)

elif risk["risk_level"] == "Medium":
    st.info("""
           
    """)
else:
    st.success("""
          
     """)
    
# patient_summary
st.markdown("---")
st.subheader("📋 Patient Summary")
summary_col1, summary_col2 = st.columns(2)
with summary_col1:
    st.write(f"***Age:*** {age} years")
    st.write(f"***Gender:*** {gender}")
    st.write(f"***State:*** {state}")
with summary_col2:
    st.write(f"***BMI:*** {bmi:.2f} kg/m²")
    st.write(f"***Number of Children:*** {children}")
    st.write(f"***Smoker:*** {smoker}")


# recommendations
st.markdown("---")
st.subheader("💡 Recommendations")
                
if risk["risk_level"] == "High":
    st.markdown("""
           
    """)
elif risk["risk_level"] == "Medium":
    st.markdown("""
       
    """)
else:
    st.markdown("""
    
    """)
    
# navigation
st.markdown("---")
button_col1, button_col2 = st.columns(2)
with button_col1:
    if st.button("🔙 Back to Prediction", use_container_width=True):
        with st.spinner("Navigating back to prediction page..."):
            st.switch_page("pages/medical_cost_predictor.py")
with button_col2:   
    if st.button("🏠 Back to Dashboard", use_container_width=True):
        with st.spinner("Navigating back to dashboard..."):
            st.switch_page("app.py")
    
# footer
st.markdown("---")
st.caption("Customer churn prediction system")