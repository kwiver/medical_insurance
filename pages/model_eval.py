import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import joblib
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

st.set_page_config(
    page_title = "Model evaluation Page",
    page_icon = "⚖️",
    layout = "wide",
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
    st.markdown("Model: Linear Regression")
    st.markdown("Version: 1.0.0")
    

st.title("⚖️ Model Evaluation: Linear Regression Metrics")
# load dataset
df = pd.read_csv("data/cleaned/cleaned_nigeria_medical_insurance.csv")

numerical_features = ["age", "bmi", "children"]
categorical_features = ["gender", "smoker", "state"]

target_column = "hospital_bill"

X = df[numerical_features + categorical_features]
y = df[target_column]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# load model
model = joblib.load("models/lr_model_pipeline.pkl")
    
# make predictions
y_pred = model.predict(X_test)
 
# calculate metrics
r2 = r2_score(y_test, y_pred)
mae = mean_absolute_error(y_test, y_pred)
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)

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
            <div style="font-size:22px; font-weight:bold; margin-top:5px;">
                {value}
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )
    
    
col1, col2, col3, col4 = st.columns(4)

with col1:
    kpi_card(
        "R² Score",
        f"{r2:.4f}",
        color="#3498db"
    )

with col2:
    kpi_card(
        "MAE",
        f"₦{mae:,.2f}",
        color="#27ae60"
        )

with col3:
    kpi_card(
        "MSE",
        f"₦{mse:,.0f}",
        color="#e74c3c"
        )
    
with col4:
    kpi_card(
        "RMSE",
        f"₦{rmse:,.0f}",
        color="#9b59b6"
        )

st.markdown("---")


# actual vs predivted bill
st.subheader("Actual vs Predicted bills")
fig = px.scatter(
    x=y_test,
    y=y_pred,
    labels={"x": "Actual bills(₦)", "y": "Predicted bills(₦)"},
    opacity=0.6
)
fig.add_trace(
    go.Scatter(
        x=[y_test.min(), y_test.max()],
        y=[y_test.min(), y_test.max()],
        mode="lines",
        name="Ideal Fit",
    )
)
st.plotly_chart(fig, use_container_width=True)

st.subheader("Residual Analysis")
residuals = y_test - y_pred

col1, col2 = st.columns(2)
# Residual Scatter plot
with col1:
    fig_res = px.scatter(
        x=y_pred,
        y=residuals,
        labels={"x": "Predicted", "y": "Residuals"},
        opacity=0.6
    )
    fig_res.add_hline(y=0)
    st.plotly_chart(fig_res, use_container_width=True)
    
# Residual Distribution
with col2:
    fig_hist = px.histogram(residuals, nbins=40, title="Residual Distribution")
    st.plotly_chart(fig_hist, use_container_width=True)

st.markdown("---")


st.subheader("Feature Importance (Linear Coefficients)")
# st.write("Top most important features based on linear coefficients")

linear_model = model.named_steps["linearregression"]
    
# Load saved model coefficients
linear_model = model.named_steps["linearregression"]
feature_names = model.named_steps["preprocessor"].get_feature_names_out()

coef_df = pd.DataFrame({
    "feature": feature_names,
    "coefficient": linear_model.coef_.ravel()
})

coef_df["abs_coefficient"] = coef_df["coefficient"].abs()
coef_df = coef_df.sort_values("abs_coefficient", ascending=True)

fig_coef = px.bar(
    coef_df,
    x="abs_coefficient",
    y="feature",
    orientation="h",
    title="Impact of Features on Medical Charges"
)

st.plotly_chart(fig_coef, use_container_width=True)

st.markdown("---")


st.subheader("Model Interpretation")

st.info("""
    • The model is primarily driven by health-risk variables (Age, BMI).  
    • Demographic features contribute secondary adjustments.  
    • Geographic pricing differences exist but are not dominant drivers.  
    • The model appears logically aligned with healthcare risk expectations.

    Overall, the linear regression model captures medically intuitive relationships 
    and shows strong interpretability, a key advantage for regulatory and insurance use cases.
    
""")

st.markdown("---")
button_col1, button_col2, button_col3 = st.columns(3, gap="medium")
with button_col1:
    if st.button("🏠 Go to Home page", use_container_width=True):
        with st.spinner("Navigating to Home page..."):
            st.switch_page("app.py")
with button_col2:   
    if st.button("📊 Go to EDA Dashboard", use_container_width=True):
        with st.spinner("Navigating back to EDA dashboard..."):
            st.switch_page("pages/eda_dashboard.py")
with button_col3:
    if st.button("🔮 Go to Predictor", use_container_width=True):
        with st.spinner("Navigating back to predictor page..."):
            st.switch_page("pages/medical_cost_predictor.py")
    

# footer
st.markdown("---")
st.caption("Medical insurance cost model evaluation")


