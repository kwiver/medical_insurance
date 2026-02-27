# 🏥 Building a Data-Driven Medical Cost Prediction System for Nigeria

## 📌 Project Overview

This project focuses on building a **Medical Insurance Cost Prediction System** tailored to the Nigerian healthcare context.

Healthcare costs in Nigeria vary significantly due to factors such as:
- Age  
- BMI  
- Smoking habits  
- Number of children  
- Gender  
- State of residence  

The goal is to build a machine learning system that can:
- Estimate hospital bills accurately  
- Identify high-risk patients  
- Reduce underwriting bias  
- Improve pricing transparency for insurance providers  

---

# 📂 Dataset Overview

**Dataset:** `nigeria_medical_insurance.csv`  
**Initial Records:** 1,472 rows  
**Initial Columns:** 7  
**Initial Data Types:** All columns were stored as `object` (strings)

### Original Columns
- Age   
-  Gender  
- BMI
- Children   
- Smoker? 
-  State   
- Hospital_Bill  

The dataset contained:
- Inconsistent column names  
- Extra spaces  
- Mixed formats (e.g., “age_45”, “23yrs”)  
- Currency symbols (₦, NGN)  
- Text-based numbers (“three”, “none”)  
- Missing values  
- Duplicate records  
- Extreme values  

---

# 🧹 PHASE 1: Data Cleaning
Data cleaning was performed systematically to ensure the dataset is reliable, consistent, and ready for modeling.

---

## 1️⃣ Fixing Column Names
- Removed leading and trailing spaces.
- Renamed all columns to lowercase.
- Standardized naming format.

Example:
- `"Age "` → `age`
- `" Gender"` → `gender`
- `"Hospital_Bill"` → `hospital_bill`

---

## 2️⃣ Cleaning Individual Columns

### 🔹 Age

**Issues Identified**
- Values like `"23yrs"`, `"age_45"`, `"30.0"`

**Steps Taken**
- Removed `"yrs"`, `"age_"`, commas, and `.0`
- Converted to numeric (`Int64`)
- Invalid values converted to `NaN`

---

### 🔹 Gender

**Issues Identified**
- `"F"`, `"fem"`, `"male"`, `"unknown"`

**Standardization**
- `"F"`, `"fem"` → `Female`
- `"M"`, `"male"` → `Male`
- `"unknown"` → `NaN`
- Trimmed extra spaces

---

### 🔹 BMI

**Issues Identified**
- `"27 kg/m2"`
- `"unknown"`
- Extra spaces and commas

**Steps Taken**
- Removed `"kg/m2"`
- Removed spaces and commas
- Converted to float
- Invalid values → `NaN`

---

### 🔹 Children

**Issues Identified**
- `"three"`
- `"none"`
- `"2.0"`

**Steps Taken**
- `"three"` → `3`
- `"none"` → `0`
- Removed commas and `.0`
- Converted to integer

---

### 🔹 Smoker

**Issues Identified**
- `"Y"`, `"N"`
- `"Smoker"`, `"Non-smoker"`
- `"?"`

**Standardization**
- `"Y"`, `"Smoker"` → `Yes`
- `"N"`, `"Non-smoker"` → `No`
- `"?"` → `NaN`
- Trimmed spaces

---

### 🔹 State

**Issues Identified**
- Extra spaces
- `"?"`

**Steps Taken**
- Capitalized values
- Removed extra spaces
- `"?"` → `NaN`

---

### 🔹 Hospital Bill

**Issues Identified**
- `"₦450,000"`
- `"NGN 1,200,000"`
- `"none"`

**Steps Taken**
- Removed `"₦"` and `"NGN"`
- Removed commas
- `"none"` → `0`
- Converted to float

---

# 🔎 Missing Value Handling

After cleaning:
- age: `260`
- gender: `360`
- bmi: `488`
- children: `239`
- smoker: `144`
- state: `143`
- hospital_bill: `222`

### Strategy Used

- **Numerical columns (age, bmi, children)** → Filled with median  
- **Gender** → Filled with mode  
- **Critical columns (smoker, state, hospital_bill)** → Dropped rows with missing values  

This ensured:
- The target variable (`hospital_bill`) has no missing values.
- Key risk indicators (`smoker`, `state`) are complete.

---

# 🔁 Duplicate Records

- Found: **89 duplicate rows**
- Action: Removed duplicates using `drop_duplicates()`

This prevents:
- Model bias
- Inflated performance metrics
- Over-representation of certain profiles

---

# 📊 Outlier Detection

Used the **IQR (Interquartile Range) Method**


### Outliers Detected

- age: `0`
- bmi: `152`
- children: `0`
- hospital_bill: `105`

---

## 🚨 Outlier Decision

Outliers were **NOT removed**.

### Reasoning

- Extreme medical costs are realistic.
- Healthcare datasets naturally contain high-cost cases.
- Removing them would:
  - Reduce dataset size significantly
  - Make the model less capable of predicting extreme cases
  - Create unrealistic cost predictions

These values represent:
- Severe medical conditions
- Surgical procedures
- High-risk smokers
- Obesity-related complications

Keeping them improves real-world robustness.

---

# 📦 Final Clean Dataset

The final dataset:

- Has standardized column names
- Contains correct data types
- Has no duplicate records
- Has no missing target values
- Retains realistic outliers

Saved as: `clean_nigeria_medical_insurance.csv`


---

# 🧠 Key Approach & Thought Process

The data cleaning approach followed three principles:

### 1️⃣ Preserve Real-World Meaning  
Medical cost data naturally contains extreme values.

### 2️⃣ Avoid Over-Cleaning  
Removing too much data weakens model generalization.

### 3️⃣ Maintain Business Relevance  
The dataset must reflect real Nigerian healthcare realities.

---


## Exploratory Data Analysis (EDA)

---

## 📌 Project Overview

This project analyzes demographic, behavioral, and regional factors that influence hospital bills.  
The goal of this Exploratory Data Analysis (EDA) is to identify patterns, relationships, and key drivers of hospital costs to guide predictive modeling.

---

# 🔎 1. Univariate Analysis

## 1.1 Age
- Range: 18 – 65 years  
- Median: ~40 years  
- Even distribution across age groups  
- No extreme outliers  

**Insight:**  
Age is well distributed and suitable for predictive modeling.

---

## 1.2 BMI
- Range: ~16 to 50+  
- Majority between 25–35  
- Slight right skew  
- Few high-BMI outliers  

**Insight:**  
BMI shows moderate variability and may influence hospital bills, especially at higher values.

---

## 1.3 Hospital Bill
- Highly right-skewed distribution  
- Majority have low to moderate bills  
- Small group with extremely high costs  

**Insight:**  
Hospital bills are not normally distributed.  
A log transformation may improve regression performance.

---

## 1.4 Smoking Status
- Smokers: ~54.5%  
- Non-smokers: ~45.5%  

**Insight:**  
Balanced distribution. Smoking status is expected to significantly influence hospital costs.

---

## 1.5 State Distribution
- Multiple states represented (Lagos, Abuja, Kano, Enugu, Rivers, Kaduna, Oyo)  
- No major imbalance observed  

**Insight:**  
Regional variation may contribute to hospital bill differences.

---

# 🔁 2. Bivariate Analysis

## 2.1 Age vs Hospital Bill
- Clear positive relationship  
- Costs increase with age  
- Higher variability among older individuals  

**Conclusion:**  
Age is positively associated with hospital expenses.

---

## 2.2 BMI vs Hospital Bill
- Weak to moderate positive relationship  
- Higher BMI associated with greater cost variability  

**Conclusion:**  
BMI influences hospital bills but is not a dominant standalone predictor.

---

## 2.3 Smoker vs Hospital Bill
- Strong visual separation between smokers and non-smokers  
- Smokers consistently incur significantly higher hospital bills  
- Most high-cost outliers are smokers  

**Conclusion:**  
Smoking status is the strongest individual predictor of hospital bills.

---

## 2.4 State vs Hospital Bill
- Average hospital bills vary across states  
- Some states show slightly higher mean costs  
- Differences are present but not extreme  

**Conclusion:**  
State contributes moderately to cost variation.

---

# 🔬 3. Multivariate Analysis

## 3.1 Correlation Analysis

Correlation findings:

- Age ↔ Hospital Bill → Moderate positive correlation (~0.25)  
- BMI ↔ Hospital Bill → Weak to moderate correlation (~0.16)  
- Children ↔ Hospital Bill → Very weak correlation  
- Low correlation among independent variables  

**Conclusion:**  
- Age has the strongest linear relationship with hospital bills.  
- Multicollinearity is not a concern.

---

## 3.2 Pairplot Insights (Age, BMI, Hospital Bill, Smoker)

- Smokers form a distinct high-cost cluster  
- Hospital bills increase sharply for smokers as age increases  
- Non-smokers show gradual cost increase  
- BMI impact strengthens when combined with smoking  

**Conclusion:**  
Feature interactions significantly impact hospital bills.

---

## 3.3 Age + Smoker + State (Facet Analysis)

- Across all states, smokers have higher hospital bills  
- Age–cost relationship is consistent across regions  
- Smoking effect is stronger than regional variation  

**Conclusion:**  
Smoking effect is dominant and consistent across states.

---

# 📈 Key Drivers Summary

## 🔥 Strong Influence
- Smoking Status  
- Age  

## ⚖ Moderate Influence
- Age  
- State  

## 📉 Weak Influence
- BMI (alone)  
- Number of Children  

---

# 🏆 Overall Findings

1. Hospital bills are highly skewed due to high-cost smokers.  
2. Smoking status is the most powerful predictor.  
3. Age shows a consistent positive relationship with hospital bills.  
4. BMI has moderate influence, especially in interaction with smoking.  
5. State variation exists but is secondary.  
6. Feature interaction effects are important drivers of cost.

---

# 🎯 Business & Modeling Implications

## Business Implications
- Smoking significantly increases healthcare cost exposure.
- Older smokers represent the highest-risk group.
- Preventive interventions targeting smoking could reduce overall costs.

## Modeling Implications
- Prioritize smoking status in feature selection.
- Include interaction terms (Age × Smoker, BMI × Smoker).
- Apply log transformation to `hospital_bill`.
- Consider outlier handling strategies.
- Tree-based models (Random Forest, Gradient Boosting) may better capture interaction effects.

---

# 🚀 Conclusion

The EDA reveals that hospital bills are primarily driven by smoking status and age.  
BMI and state contribute moderately, while feature interactions amplify cost effects.

These insights provide a strong foundation for building a robust and accurate predictive model.




# 📊 PHASE 4: MODEL INTERPRETATION  
Medical Insurance / Hospital Bill Prediction

---

# 1️⃣ Overview

This phase evaluates and interprets three trained models:

- **Linear Regression**
- **Random Forest Regressor**
- **XGBoost Regressor**

Dataset Summary:
- 927 records
- 6 input features:
  - age
  - gender
  - bmi
  - children
  - smoker
  - state
- Target variable: `hospital_bill`
- Mean hospital bill: ₦19.6M
- Max hospital bill: ₦95.6M

---

# 2️⃣ Model Performance Comparison

| Model | Test R² | CV Mean R² | Test MAE |
|-------|----------|------------|----------|
| Linear Regression | 0.0966 | 0.0353 | ₦13M |
| Random Forest | 0.0565 | 0.0436 | ₦13M |
| XGBoost | 0.0720 | **0.0569** | ₦13M |

### 🔎 Interpretation

- All models explain **less than 10% of variance**.
- XGBoost generalizes slightly better (highest CV mean).
- Random Forest shows slight overfitting (train R² > test R²).
- Prediction errors (~₦13M MAE) are large relative to mean bill (~₦19M).

⚠️ Conclusion: The dataset lacks strong predictive drivers (e.g., disease severity, treatment type, admission duration).

---

# 3️⃣ Feature Importance Analysis

## 🔹 A) Linear Regression (Magnitude-Based Interpretation)

Top Influencing Features (by coefficient size):

1. **Age** (+₦4.12M per year)
2. **BMI** (+₦2.36M per unit)
3. **State**
4. **Smoking**
5. Children
6. Gender (very small effect)

### Key Insight

- Age is the strongest linear predictor.
- BMI is the second strongest.
- Geographic location impacts cost moderately.
- Gender has minimal financial impact.

---

## 🔹 B) Random Forest Feature Importance

| Feature | Importance |
|----------|------------|
| Age | 0.41 |
| BMI | 0.30 |
| Children | 0.07 |
| Smoking | ~0.05 combined |
| State | ~0.11 combined |
| Gender | ~0.04 |

### Interpretation

Random Forest confirms:

- **Age and BMI dominate predictions (71% combined importance).**
- Children has moderate influence.
- Smoking contributes modestly.
- Gender has weak impact.

Tree models capture non-linear patterns, suggesting:
- Cost increases accelerate at higher age ranges.
- High BMI patients may incur disproportionately higher costs.

---

## 🔹 C) XGBoost Feature Importance

| Feature | Importance |
|----------|------------|
| Age | 0.176 |
| BMI | 0.152 |
| State (combined) | High cumulative influence |
| Children | 0.084 |
| Smoking | ~0.096 combined |
| Gender | Lower influence |

### Interpretation

- XGBoost spreads importance more evenly.
- State plays a stronger role than in Random Forest.
- Age and BMI remain primary drivers.
- Children importance increases relative to Random Forest.

---

# 4️⃣ Which Factors Influence Medical Costs Most?

Across all three models:

### 🔥 Primary Drivers
1. **Age**
2. **BMI**

### 🟡 Secondary Drivers
3. State
4. Smoking
5. Number of Children

### 🔵 Minor Driver
6. Gender

---

# 5️⃣ High-Cost Risk Patterns Identified

Based on model behavior:

### 🚨 High-Risk Profile

Patients likely to incur higher hospital bills:

- Older individuals (50+ years)
- High BMI (>35)
- Smokers
- Residents of higher-cost states (e.g., Abuja, Enugu in linear model)
- Families with multiple dependents

### 💡 Pattern Insight

Cost appears to increase with:
- Aging-related conditions
- Obesity-related complications
- Regional pricing differences

Tree-based models suggest **non-linear escalation**, meaning:
- Costs may rise sharply beyond certain BMI or age thresholds.

---

# 6️⃣ Fairness & Bias Implications

## ⚖️ Gender

- Minimal influence across all models.
- Low risk of gender-based pricing bias.

## 🌍 State (Geographic Bias Risk)

- State has measurable impact.
- Could reflect:
  - Healthcare infrastructure differences
  - Regional cost of services
  - Insurance pricing disparities

⚠️ Ethical Concern:
If deployed in pricing decisions, the model could indirectly penalize individuals based on location.

## 🚬 Smoking

- Higher costs associated with smokers.
- From an actuarial standpoint, medically justified.
- However, must ensure compliance with insurance regulation standards.

---

# 7️⃣ Why Model Performance is Low

Despite meaningful feature importance:

- R² < 0.10 suggests missing variables.
- Hospital bills likely driven by:
  - Type of illness
  - Hospital type (public vs private)
  - Length of admission
  - Surgical procedures
  - Emergency vs elective care

Current features capture only demographic risk, not clinical complexity.

---

# 8️⃣ Overall Model Interpretation Summary

| Insight | Conclusion |
|----------|------------|
| Strongest predictors | Age and BMI |
| Moderate predictors | State, Smoking |
| Weak predictor | Gender |
| Model reliability | Low explanatory power |
| Risk of bias | Moderate geographic bias |
| Business usability | Limited without additional features |

---

# 9️⃣ Final Professional Assessment

- All models consistently identify **age and BMI as dominant cost drivers**.
- Tree-based models capture some non-linearity but do not significantly improve predictive power.
- Geographic location introduces potential fairness concerns.
- Model performance indicates substantial missing explanatory variables.

### Recommendation for Improvement:

- Add clinical variables (diagnosis, admission days, treatment type).
- Log-transform hospital_bill.
- Perform SHAP analysis for XGBoost for deeper interpretability.
- Conduct bias testing by state and smoking status.

---

# ✅ Conclusion

The models successfully identify demographic and lifestyle patterns associated with higher medical costs. However, due to low predictive power, they should not be used for financial decision-making without additional medical and operational features.
