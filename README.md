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