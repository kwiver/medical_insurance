# Data Cleaning Process — Nigeria Medical Insurance Dataset

## Overview

This document outlines the data cleaning steps applied to the raw medical insurance dataset in preparation for model training and EDA. Two versions of the cleaned dataset were produced:

- `data/cleaned/cleaned_nigeria_medical_insurance.csv` — for model training (missing values retained)
- `data/cleaned/cleaned_nigeria_medical_insurance_1.csv`- an imputed copy of the above, for EDA only

---

## Raw Dataset

- **Shape:** 1,472 rows × 7 columns
- **Dtypes:** All columns loaded as `object`
- **Missing values:** Present across 5 of 7 columns
- **Issues:** Inconsistent formatting — unit suffixes (`yrs`, `kg/m2`, `₦`, `NGN`), leading/trailing whitespace, mixed casing, text-encoded values (`three`, `none`, `non-smoker`), and placeholder characters (`?`)

---

## Cleaning Steps

### 1. Column-by-Column Cleaning

Each column required a tailored cleaning approach:

- **`age`** — stripped suffixes (`yrs`, `age_`), removed commas and `.0`, cast to `Int64`
- **`gender`** — standardised abbreviations (`F` → `Female`, `M` → `Male`), capitalised, `unknown` → `NaN`
- **`bmi`** — stripped `kg/m2` and whitespace, `unknown` → `NaN`, cast to `float`
- **`children`** — converted text numbers (`three` → `3`, `none` → `0`), removed `.0`, cast to `Int64`
- **`smoker`** — capitalised, standardised variants (`Non-smoker` → `No`, `Smoker` → `Yes`, `Y`/`N`, `?` → `NaN`)
- **`state`** — stripped whitespace, capitalised, `?` → `NaN`
- **`hospital_bill`** — stripped currency symbols (`₦`, `NGN`) and commas, `none` → `0`, cast to `float`

---

### 2. Dropping Rows with Missing Critical Values

Rows missing `smoker`, `state`, or `hospital_bill` were dropped, as these are either the target variable or essential identifiers that cannot be reliably imputed.

```python
df = df.dropna(subset=["smoker", "state", "hospital_bill"])
```

---

### 3. Filtering Outliers

Two filters were applied to remove extreme values likely to distort model training:

```python
df = df[df["bmi"] <= 45]
df = df[df["hospital_bill"] <= 3_800_000]
```

> After applying these filters, no significant outliers remained in the dataset.

**Final shape after cleaning: 554 rows × 7 columns**

---

### 4. Export — Model-Ready Dataset

```python
df.to_csv("data/cleaned/cleaned_nigeria_medical_insurance.csv", index=False)
```

> Remaining missing values in `age`, `bmi`, `children`, and `gender` are **intentionally retained** to avoid data leakage. They will be handled within the model pipeline using `SimpleImputer`.

---

## EDA Dataset — Manual Imputation

A separate imputed copy was prepared for EDA only, using the same strategy that will be applied by `SimpleImputer` in the model pipeline.

**Imputation applied:**
- `bmi` → median
- `age` → median
- `children` → median
- `gender` → `"Unknown"`

---

### 5. Deduplication

```python
df.duplicated().sum()  # → 50 duplicates found
df = df.drop_duplicates()
```

---

## Smoker Distribution (Post-Cleaning)

The cleaned dataset shows a near-even split between smokers and non-smokers:

- `Yes` (smoker) — 268 records
- `No` (non-smoker) — 236 records

This balance is notable, as smoking status is expected to be a strong predictor of hospital bill cost.

---

## Final Summary

- **Raw data:** 1,472 rows, all columns as `object`, heavily malformatted
- **After dropping critical nulls and filtering:** 554 rows × 7 columns
- **After deduplication:** 50 duplicate rows removed
- **For modelling:** missing values in `age`, `bmi`, `children`, `gender` retained for `SimpleImputer`
- **For EDA:** missing values filled with median (numeric) or `"Unknown"` (categorical)


# Exploratory Data Analysis — Nigeria Medical Insurance Dataset

## Overview

This document summarises the key findings from the EDA conducted on the imputed version of the cleaned dataset. The analysis covers univariate, bivariate, and multivariate perspectives to understand the data structure and feature relationships with the target variable `hospital_bill`.

- **Source:** `data/cleaned/cleaned_nigeria_medical_insurance_1.csv`
- **Shape:** 927 rows × 7 columns
- **Missing values:** None (imputed prior to EDA)

---

## Descriptive Statistics

Key statistics for numeric features:

- `age` — mean ~39.4, std ~12.7, range 18–64
- `bmi` — mean ~30.8, std ~4.9, range 16–53.1
- `children` — mean ~1.3, range 0–5
- `hospital_bill` — mean ~₦19.6M, std ~₦18.1M, range ₦1.7M–₦95.7M

The high standard deviation on `hospital_bill` relative to its mean confirms a wide and skewed cost distribution across patients.

---

## Univariate Analysis

### Age Distribution

The boxplot shows age is broadly distributed between 29 and 49 with a median around 40. The range spans 18 to 64 with no extreme outliers. The distribution is fairly symmetric, suggesting a well-spread patient population across age groups.

### BMI Distribution

The histogram reveals a strongly peaked, right-skewed distribution centred around BMI 28–30. The majority of patients fall in the 25–35 range, consistent with an overweight-to-obese classification. Very few patients fall below 20 or above 45, the latter having been filtered during cleaning.

### Hospital Bill Distribution

The histogram is heavily right-skewed. Most bills cluster below ₦20M, but a significant tail extends toward ₦80M–₦100M. This confirms that while most patients incur moderate costs, a smaller subset drives disproportionately high expenditure — a pattern relevant for risk segmentation.

### Smoker Proportion

The pie chart shows a near-even split in the dataset:

- **Smokers (Yes):** 54.5%
- **Non-smokers (No):** 45.5%

---

## Bivariate Analysis

### Age vs Hospital Bill

The scatter plot shows a weak but visible positive trend, older patients tend to incur higher bills, particularly above age 40 where costs spread more widely toward the upper range. The relationship is non-linear and dispersed, indicating age alone is not a strong standalone predictor.

### BMI vs Hospital Bill

A moderate positive relationship is visible — higher BMI patients tend to incur higher bills, particularly above BMI 30. The spread is wide, suggesting BMI interacts with other factors (notably smoking) to drive cost rather than acting independently.

### Smoker vs Hospital Bill

The grouped mean hospital bill by smoker status shows:

- **Smokers:** mean ~₦19.9M
- **Non-smokers:** mean ~₦19.2M

While smokers carry a higher average bill, the difference is modest in absolute terms. However, the total bill sum shows a larger gap, smokers collectively account for ~₦10.0B versus ~₦8.1B for non-smokers — reflecting both higher individual costs and higher representation in the dataset. The scatter plot shows no clear visual separation between groups, suggesting smoking's effect is stronger in combination with other features.

### State vs Hospital Bill

The horizontal bar chart of mean hospital bill by state reveals:

- **Enugu** records the highest mean hospital bill
- **Abuja** and **Kano** follow closely
- **Kaduna** has the lowest mean bill among the seven states

The differences between states are meaningful and suggest geographic or provider-level cost variation worth investigating further.

---

## Multivariate Analysis

### Correlation Heatmap

The heatmap of numeric features shows:

- `age` has the strongest correlation with `hospital_bill` at **0.25**
- `bmi` follows at **0.16**
- `children` shows near-zero correlation with `hospital_bill` at **0.04**
- `age` and `bmi` share a mild positive correlation of **0.13**
- No severe multicollinearity detected among features

Overall, numeric correlations with `hospital_bill` are weak, indicating that categorical features — particularly `smoker` and `state` — likely carry significant predictive weight that linear correlation does not capture.

### Pairplot (Age, BMI, Hospital Bill by Smoker)

The pairplot coloured by smoker status reveals that smokers and non-smokers are largely overlapping across age and BMI distributions. The `hospital_bill` distribution for both groups is similarly right-skewed. There is no clean visual separation by smoking status in the pairplot alone, reinforcing that smoking's predictive power is likely interaction-dependent rather than marginal.

### Age × State × Smoker (Faceted Scatter)

Faceting age vs hospital bill by state and colouring by smoker status shows consistent patterns across all seven states — older patients and smokers tend to appear at higher bill values regardless of location. Enugu and Abuja show more pronounced high-bill outliers. The smoker vs non-smoker overlap is present in every state, confirming no single state drives the smoking-cost relationship disproportionately.

### BMI × State × Smoker (Faceted Scatter)

Faceting BMI vs hospital bill by state shows that high-BMI patients (above 35) tend to cluster at higher bill amounts across most states. The pattern is most pronounced in Lagos and Abuja. Again, smoker and non-smoker points are interleaved across BMI ranges, suggesting BMI and smoking together — rather than either alone — drive the highest-cost cases.

---

## Key Takeaways

- `hospital_bill` is **right-skewed** with a wide range, a regression model must account for this distribution
- **Age** is the strongest numeric predictor (r = 0.25), followed by **BMI** (r = 0.16)
- **Smoking status** contributes meaningfully but its effect appears strongest in combination with age and BMI, not in isolation
- **State** introduces geographic cost variation, with Enugu and Abuja showing consistently higher average bills
- **Children** shows negligible correlation with cost and may contribute little predictive value
- No strong multicollinearity exists among numeric features


