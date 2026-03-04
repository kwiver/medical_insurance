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






# Model Evaluation & Comparison — Nigeria Medical Insurance Dataset

## Overview

Three regression models were trained and evaluated to predict `hospital_bill`. All models shared the same train/test split of 443 training samples and 111 test samples, with a target price range of ₦1.7M–₦37.6M (train) and ₦1.7M–₦37.9M (test).

The baseline MAE of **₦7,326,495.53** serves as the benchmark, any model that fails to beat this is no better than simply predicting the mean for every patient.

Given the right-skewed nature of `hospital_bill`, **R² on log scale** is treated as the primary evaluation metric alongside MAE, as it better reflects model performance on skewed targets.

---

## Model 1 — Linear Regression

**Coefficients (top drivers by absolute value):**
- `age` — +4,008,250.49 *(strongest positive driver)*
- `children` — +953,530.84
- `bmi` — -844,294.88
- `state_Rivers` — -1,892,643.42
- `state_Abuja` — +1,006,911.72
- `smoker_No` / `smoker_Yes` — ±767,562.21

**Evaluation results:**

- Training R² — 0.2165 | R² (log scale): not reported
- Testing R² — 0.1604
- Training RMSE — ₦7.9M | MAE — ₦5.8M
- Testing RMSE — ₦8.7M | MAE — ₦6.4M
- CV R² mean — 0.1524 ± 0.1068

**Observation:** Linear Regression performs poorly. A test R² of 0.1604 means the model explains only 16% of variance in hospital bills. Its test MAE of ₦6.4M is only marginally better than the baseline of ₦7.3M, and the high CV standard deviation (0.1068) indicates unstable generalisation across folds. The model's inability to capture non-linear relationships limits it significantly given the skewed target and interaction-heavy feature set.

---

## Model 2 — Random Forest

**Feature importance:**
- `age` — 0.732 *(dominant predictor by a wide margin)*
- `bmi` — 0.110
- `children` — 0.059
- `state` — 0.047
- `smoker` — 0.030
- `gender` — 0.021

**Evaluation results:**

- Training R² (original scale) — 0.2778 | R² (log scale) — 0.5067
- Testing R² (original scale) — 0.0972 | R² (log scale) — 0.3410
- Training RMSE — ₦7,594,305.97 | MAE — ₦4,567,184.96
- Testing RMSE — ₦8,991,953.82 | MAE — ₦5,760,038.60
- CV R² mean (log scale) — 0.3070 ± 0.1085

**Observation:** Random Forest shows a reasonable log-scale R² of 0.3410 on the test set, significantly better than Linear Regression. Its training MAE of ₦4.6M is strong, but the gap between training R² (0.2778) and test R² (0.0972) on the original scale signals some overfitting. Performance is more stable when evaluated on the log scale, which better suits the skewed distribution of hospital bills. The CV mean of 0.3070 confirms moderate generalisation.

---

## Model 3 — XGBoost

**Feature importance:**
- `age` — 0.391 *(strongest predictor)*
- `bmi` — 0.188
- `smoker` — 0.134
- `children` — 0.128
- `state` — 0.099
- `gender` — 0.059

**Evaluation results:**

- Training R² — 0.2682 | RMSE — ₦7.6M | MAE — ₦5.8M
- Testing R² — 0.1827 | RMSE — ₦8.6M | MAE — ₦6.5M
- CV R² mean — 0.1629 ± 0.0661

**Observation:** XGBoost achieves the best test R² on the original scale (0.1827) among all three models and has the lowest CV standard deviation (0.0661), indicating it is the most stable and consistent performer across folds. While its absolute error metrics are comparable to the others, its tighter CV spread and better original-scale test R² suggest it generalises most reliably to unseen data.

---

## Model Comparison Summary

- **Test R² (original scale):** XGB 0.1827 > LR 0.1604 > RF 0.0972
- **Test R² (log scale):** RF 0.3410 > XGB not reported > LR not reported
- **Test MAE:** LR ₦6.4M ≈ XGB ₦6.5M < RF ₦5.8M (train only; test ₦5.76M)
- **CV R² mean:** RF 0.3070 (log) > XGB 0.1629 > LR 0.1524
- **CV stability (std):** XGB ±0.0661 > LR ±0.1068 > RF ±0.1085
- **Baseline MAE beat:** All three models beat the ₦7.3M baseline on MAE

> Overall, all three models show modest predictive performance, which is expected given the small dataset size (554 rows), the right-skewed target, and the limited feature set. None of the models achieve strong R² on the original scale, suggesting meaningful variance in hospital bills remains unexplained by the available features.

---

## Best Model — XGBoost

**XGBoost is selected as the best model** for the following reasons:

**1. Highest test R² on original scale.** XGBoost achieves 0.1827 on the test set, compared to 0.1604 for Linear Regression and 0.0972 for Random Forest, meaning it explains the most variance in unseen hospital bill data.

**2. Most stable cross-validation performance.** Its CV standard deviation of ±0.0661 is substantially lower than both Random Forest (±0.1085) and Linear Regression (±0.1068), confirming it generalises most consistently across different data splits.

**3. More balanced feature importance.** Unlike Random Forest, which assigns 73% of importance to age alone, XGBoost distributes importance more evenly across age (0.391), bmi (0.188), smoker (0.134), and children (0.128). This suggests it is learning a richer set of patterns rather than over-relying on a single feature.

**4. No meaningful overfitting.** The gap between training R² (0.2682) and test R² (0.1827) is the smallest among the tree-based models, indicating better balance between fit and generalisation.

Random Forest performs well on the log scale (R² 0.3410) and may be worth revisiting with log-transformed target training. Linear Regression is too weak and too unstable for deployment. All models would benefit significantly from a larger dataset and additional features such as diagnosis type, hospital tier, and insurance coverage status.






# Model Interpretation — XGBoost (Medical Insurance)

## Overview

This section interprets the XGBoost model selected as the best performer for predicting hospital bill costs. The goal is to understand which features drive cost predictions, identify high-cost patient profiles, and examine the fairness implications of using this model in a medical insurance or billing context.

---

## Feature Importance

XGBoost ranks features by their average contribution to prediction splits across all boosting rounds. The full feature importance ranking is:

- `age` — 0.391 *(dominant predictor)*
- `bmi` — 0.188
- `smoker` — 0.134
- `children` — 0.128
- `state` — 0.099
- `gender` — 0.059

A notable strength of XGBoost over Random Forest in this dataset is the more balanced distribution of importance, age accounts for 39% rather than the 73% seen in Random Forest, meaning the model draws meaningful signal from all six features rather than over-relying on one.

---

## Factors That Influence Medical Cost Most

### 1. Age (0.391 — Strongest Driver)

Age is the most influential predictor of hospital bill cost by a significant margin. Older patients consistently incur higher bills, with the scatter plots from EDA confirming a positive trend that becomes more pronounced above age 40. This reflects the well-established relationship between age and healthcare utilisation, older patients tend to present with more complex, chronic, or severe conditions requiring more intensive and costly treatment.

### 2. BMI (0.188 — Second Driver)

Higher BMI is the second strongest cost driver. Patients with BMI above 30, classified as obese tend to incur higher bills, a pattern visible in the EDA scatter plots across all states. Elevated BMI is associated with conditions such as hypertension, diabetes, and cardiovascular disease, all of which increase treatment complexity and cost. The relationship is not strictly linear, suggesting the model is capturing non-linear threshold effects that Linear Regression could not.

### 3. Smoking Status (0.134)

Smoking contributes meaningfully to cost prediction. While the EDA showed only a modest ₦700k gap in mean bills between smokers and non-smokers, the XGBoost model assigns it 13.4% importance, suggesting that smoking's effect is strongest in combination with other features, particularly age and BMI. A smoker with high BMI and older age is likely to attract a substantially higher predicted cost than each factor alone would suggest.

### 4. Number of Children (0.128)

Children is the fourth most important feature, carrying importance comparable to smoking status. This is somewhat counterintuitive, having dependants does not directly raise personal medical costs. It likely acts as a proxy for broader household or lifestyle factors, such as stress, reduced physical activity, or healthcare access patterns, that correlate with higher bills in this dataset.

### 5. State (0.099)

Geographic location contributes ~10% of predictive importance, consistent with the EDA finding that Enugu and Abuja showed the highest mean bills while Kaduna had the lowest. This reflects real variation in healthcare costs across Nigerian states, driven by differences in hospital infrastructure, provider pricing, cost of living, and availability of specialist care.

### 6. Gender (0.059)

Gender is the least important feature at 5.9%. Its presence in the model introduces fairness considerations discussed below, though its low importance suggests it contributes limited marginal predictive value beyond what other features already capture.

---

## High-Cost Risk Patterns

Based on feature importance scores and EDA findings, a high-cost patient profile looks as follows:

- **Older age**, typically above 50
- **High BMI**, above 35 (obese class II or above)
- **Active smoker**
- **Multiple children** (3 or more)
- **Located in Enugu or Abuja** : states with the highest average bills
- **Male gender** — given the positive coefficient direction observed in the Linear Regression model, though the effect is modest

The interaction of age, BMI, and smoking status is the most dangerous combination. A patient who is older, obese, and a smoker is likely to sit at the extreme upper end of predicted costs, potentially in the ₦50M–₦95M range based on the distribution seen in EDA. State amplifies this further when the patient is located in a high-cost geography.

Conversely, younger non-smoking patients with low BMI and few or no children located in Kaduna or Rivers represent the lowest-cost profile.

---

## Fairness and Bias Implications

### Age

Age is the strongest predictor and its use in cost prediction is medically justified, older patients genuinely incur higher treatment costs on average. However, in an insurance pricing context, using age as a primary cost driver can lead to premiums that are unaffordable for older individuals who may already be on fixed incomes. Regulatory frameworks in many countries restrict age-based pricing for this reason, and similar considerations are relevant in the Nigerian context.

### Gender

Gender appears in the model with an importance of 5.9%. Its inclusion means predicted costs, and potentially insurance premiums derived from those predictions vary by gender. This raises equity concerns, particularly if gender is acting as a proxy for underlying clinical or socioeconomic patterns rather than contributing direct medical signal. Removing gender and re-evaluating performance impact is advisable before deployment, as the marginal predictive gain is small relative to the fairness cost.

### BMI

BMI is a medically relevant feature, but its use can introduce indirect bias. BMI distributions are not uniform across socioeconomic groups, lower-income populations tend to have higher BMI on average due to factors like food access, stress, and limited time for exercise. A model that penalises high BMI in pricing or coverage decisions may therefore disproportionately burden already disadvantaged groups, even when the intent is purely actuarial.

### Children

The use of number of children as a cost predictor warrants scrutiny. If it is acting as a proxy for socioeconomic status or household stress rather than direct medical causation, it risks penalising patients for demographic characteristics unrelated to clinical need. Its causal role should be investigated before retaining it in a production model.

### Geographic Bias (State)

State-level cost variation reflects real infrastructure and pricing differences, but using state as a feature can produce systematically higher predicted costs — and therefore higher premiums, for patients in Enugu or Abuja regardless of their individual health profile. Patients in high-cost states who are otherwise healthy may face unfair pricing penalties simply due to where they live.

### Small Dataset Risk

With only 554 training samples, the model's learned patterns may reflect noise or historical biases in the data collection process rather than true clinical relationships. Predictions should be treated as indicative rather than definitive, and the model should be retrained as more data becomes available.

### Recommendations

- **Audit gender** as an input feature, remove it and measure the performance impact before deciding whether to retain it
- **Investigate children** as a potential socioeconomic proxy, consider replacing it with a more direct clinical or financial variable
- **Apply model outputs with human oversight** in any insurance pricing or risk stratification context, particularly for high-cost predictions that may trigger coverage restrictions
- **Collect more data** — 554 rows is insufficient for a robust production model; a larger and more representative dataset would reduce bias risk and improve generalisation
- **Monitor for disparate impact** by evaluating predicted costs across age bands, gender, and state to detect systematic over- or under-estimation for specific groups
