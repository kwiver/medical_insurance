import streamlit as st

st.set_page_config(
    page_title = "Prediction Result",
    page_icon = "📄",
    layout = "centered",
    initial_sidebar_state = "expanded"
)

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
    
# footer
st.markdown("---")
st.caption("Customer churn prediction system")