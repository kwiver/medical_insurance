import streamlit as st
import numpy as np
import pandas as pd
import joblib

# page config
st.set_page_config(
    page_title = "Medical Bill Prediction System",
    page_icon = "🏥",
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
    st.page_link("app.py",                label="🏠 Home",               )
    st.page_link("pages/eda_dashboard.py",           label="📊 EDA Dashboard",      )
    st.page_link("pages/medical_cost_predictor.py",    label="🔮 Medical Cost Predictor",       )
    st.page_link("pages/model_eval.py",       label="⚖️ Model Evaluation", )
    st.markdown("---")
    st.markdown("**Project Info**")
    st.markdown("Dataset: `nigeria_medical_insurance.csv`")
    st.markdown("Model: Regression ensemble")
    st.markdown("Version: 1.0.0")

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
    try:
        model = joblib.load("models/lr_model_pipeline.pkl")
        return model
    except FileNotFoundError as e:
        st.error(f"Model artifact not found: {e}")
        st.error("Please ensure lr_model_pipeline.pkl exists inside models directory.")
        st.stop()
    except Exception as e:
        st.error(f"Error loading model: {e}")
        st.stop()

        
@st.cache_data()
def load_dataset():
    try:
        df = pd.read_csv("data/cleaned/cleaned_nigeria_medical_insurance.csv")
        return df
    except FileNotFoundError as e:
        st.error(f"Dataset not found {e}")
        st.stop()
    except Exception as e:
        st.error(f"Error loading dataset: {e}")
        st.stop()

def predict_bill(patient_data, model):
    
    try:
        input_df = pd.DataFrame([patient_data])
        predicted_bill = model.predict(input_df)[0]
        
        return predicted_bill
    
    except Exception as e:
        st.error(f"Prediction error: {e}")


def calculate_risk(age, bmi, smoker):
    score = 0

    # Age scoring
    if age < 30:
        score += 0
    elif 30 <= age <= 50:
        score += 1
    else:
        score += 2

    # BMI scoring
    if bmi < 25:
        score += 0
    elif 25 <= bmi <= 30:
        score += 1
    else:
        score += 2

    # Smoker scoring
    if smoker == "Yes":
        score += 3

    # Determine risk level
    if score <= 2:
        risk_level = "Low"
        risk_color = "🟢"
    elif score <= 4:
        risk_level = "Medium"
        risk_color = "🟡"
    else:
        risk_level = "High"
        risk_color = "🔴"
    
    risk = {
            "risk_level": risk_level,
            "risk_color": risk_color
    }
    
    return risk


def main():
    # header
    st.title("🏥 Medical Bill Prediction System")
    st.write("Fill all the fields and get immediate result.")
    
    # load model and dataset
    model = load_model()

    df = load_dataset()
           
    st.markdown("---")
    st.subheader("Enter Patient Details")
    
    col1, col2 = st.columns(2)
    with col1:
        age = st.number_input(
            "Age",
            min_value=20, 
            max_value=85, 
            value=25,
            help="Patient age"
        )
        
        gender = st.selectbox(
            "Gender",
            options=["Male", "Female"],
            help="Patient's gender"
        )
        
        state = st.selectbox(
            "State",
            options=["Lagos", "Abuja", "Rivers", "Kano", "Kaduna", "Oyo", "Enugu", "Anambra", "Edo", "Delta"],
            help="State of residence"
        )
    
    with col2:
        bmi = st.number_input(
            "BMI",
            min_value=15.0, 
            max_value=50.0, 
            value=22.0,
            step=1.0,
            help="Body Mass Index"
        )
        
        children = st.number_input(
            "Number of Children",
            min_value=0, 
            max_value=10, 
            value=0,
            step=1,
            help="Number of children/dependents"
        )
        
        smoker = st.selectbox(
            "Smoker",
            options=["Yes", "No"],
            help="Whether the patient is a smoker or not"
        )
        
    # get result
    if st.button("Predict Medical Bill", type="primary", use_container_width=True):
        
        if age is None or gender is None or state is None or bmi is None or smoker is None:
            st.warning("⚠️ Please fill all the fields")
        else:
            patient_data = {
                "age": age,
                "gender": gender,
                "state": state,
                "bmi": bmi,
                "children": children,
                "smoker": smoker
            }
            with st.spinner("Calculating predicted bill..."):
                result = predict_bill(patient_data, model)
                risk = calculate_risk(age, bmi, smoker)
                if result is not None:

                    # Save prediction
                    st.session_state.predicted_bill = result
                    
                    # save risk
                    st.session_state.calculate_risk = risk

                    # Save patient data 
                    st.session_state.age = age
                    st.session_state.bmi = bmi
                    st.session_state.smoker = smoker
                    st.session_state.gender = gender
                    st.session_state.state = state
                    st.session_state.children = children
                    
                # Switch page
                st.switch_page("pages/prediction_result.py")
              
    # footer
    st.markdown("---")
    st.caption("Customer churn prediction system")
        
if __name__  ==  "__main__":
    main()