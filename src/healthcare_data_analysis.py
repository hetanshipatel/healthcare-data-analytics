# %% [markdown]
# # Healthcare Data Analytics – Cleaned Data Inspection
# 
# ## 1. Load and Validate Cleaned Dataset

# %%

# Import required libraries

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display

from pathlib import Path

# Locate the project folder
possible_roots = [Path.cwd(), Path.cwd().parent]

project_root = next(
    (p for p in possible_roots
     if (p / "data" / "processed" / "diabetic_data_cleaned.csv").exists()),
    None
)

if project_root is None:
    raise FileNotFoundError(
        "Could not find diabetic_data_cleaned.csv in data/processed"
    )

# Load the cleaned dataset
file_path = (
    project_root / "data" / "processed" /
    "diabetic_data_cleaned.csv"
)

df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)

display(df.head())


# %% [markdown]
# ## 2. Dataset Validation

# %%

# Check dimensions
print("Rows:", df.shape[0])
print("Columns:", df.shape[1])

# Check missing values
print("\nTotal missing values:", df.isna().sum().sum())

# Check completely duplicated records
print("Duplicate rows:", df.duplicated().sum())

# Check unique encounters and patients
print("Unique encounters:", df["encounter_id"].nunique())
print("Unique patients:", df["patient_nbr"].nunique())

# Check the new engineered features
engineered_features = [
    "total_prior_visits",
    "medication_count",
    "medication_change_flag",
    "diabetes_medication_flag"
]

display(df[engineered_features].describe())


# %% [markdown]
# ## 3. Readmission Distribution

# %%
# Count each readmission category
readmission_counts = df["readmitted"].value_counts()

display(readmission_counts)

# Calculate percentages
readmission_percentage = (
    df["readmitted"].value_counts(normalize=True) * 100
).round(2)

display(readmission_percentage)

# %%
print("Total columns:", len(df.columns))
display(pd.DataFrame({
    "Column_Name": df.columns,
    "Data_Type": df.dtypes.astype(str).values
}))

# %% [markdown]
# ## 4. Exploratory Data Analysis
# 
# ### 4.1 Patient Demographics

# %%
#A. Age distribution

age_order = [
    "[0-10)", "[10-20)", "[20-30)", "[30-40)",
    "[40-50)", "[50-60)", "[60-70)", "[70-80)",
    "[80-90)", "[90-100)"
]

plt.figure(figsize=(12, 6))

sns.countplot(
    data=df,
    x="age",
    order=age_order
)

plt.title("Hospital Encounters by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Encounters")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# %%
# B. Gender distribution
gender_counts = df["gender"].value_counts()
print(gender_counts)

plt.figure(figsize=(7, 5))

sns.barplot(
    x=gender_counts.index,
    y=gender_counts.values
)

plt.title("Hospital Encounters by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()

# %%
#C. Race distribution
race_counts = df["race"].value_counts()

plt.figure(figsize=(10, 6))

sns.barplot(
    x=race_counts.values,
    y=race_counts.index
)

plt.title("Hospital Encounters by Recorded Race")
plt.xlabel("Number of Encounters")
plt.ylabel("Race")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 5. Hospital Activity Analysis

# %%
# 5.1 Length of hospital stay
# Convert to numeric
df["time_in_hospital"] = pd.to_numeric(
    df["time_in_hospital"], errors="coerce"
)

# Summary statistics
print("Hospital stay summary:")
display(df["time_in_hospital"].describe())

# Distribution chart
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="time_in_hospital",
    bins=14,
    kde=True
)

plt.title("Distribution of Hospital Stay Duration")
plt.xlabel("Days in Hospital")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()

# %%
# 5.2 Number of laboratory procedures
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="num_lab_procedures",
    bins=30,
    kde=True
)

plt.title("Distribution of Laboratory Procedures")
plt.xlabel("Number of Lab Procedures")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()

display(df["num_lab_procedures"].describe())

# %%
#5.3 Number of medical procedures
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="num_procedures",
    bins=15,
    discrete=True
)

plt.title("Distribution of Medical Procedures")
plt.xlabel("Number of Procedures")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()

# %%
# 5.4 Number of medications
plt.figure(figsize=(10, 5))

sns.histplot(
    data=df,
    x="num_medications",
    bins=30,
    kde=True
)

plt.title("Distribution of Medications per Encounter")
plt.xlabel("Number of Medications")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()

# %%
#5.5 Previous hospital visits
plt.figure(figsize=(10, 5))

sns.countplot(
    data=df,
    x="total_prior_visits"
)

plt.title("Previous Healthcare Visits per Encounter")
plt.xlabel("Total Previous Visits")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()

# %%
#5.6 Compare hospital stay with readmission
plt.figure(figsize=(10, 6))

sns.boxplot(
    data=df,
    x="readmitted",
    y="time_in_hospital",
    order=["NO", ">30", "<30"]
)

plt.title("Hospital Stay Duration by Readmission Category")
plt.xlabel("Readmission Category")
plt.ylabel("Days in Hospital")
plt.tight_layout()
plt.show()

# %% [markdown]
# ## 6. Readmission Analysis
# 
# ### 6.1 Create the readmission target
# ### 6.2 Overall readmission distribution
# ### 6.3 Readmission by age group
# ### 6.4 Readmission by gender and race
# ### 6.5 Admission type and discharge destination
# ### 6.6 Previous visits and medication count
# ### 6.7 Readmission by Medication Count

# %%

# 6.1 Create the readmission target
#  Convert readmission into a binary target

df["readmission_30d"] = (
    df["readmitted"].eq("<30").astype(int)
)

print("Readmission target created.")

display(
    df["readmission_30d"].value_counts()
)

display(
    (df["readmission_30d"].value_counts(normalize=True) * 100)
    .round(2)
)


# %%
# 6.2 Overall readmission distribution

readmission_counts = df["readmitted"].value_counts()

plt.figure(figsize=(8, 5))

sns.barplot(
    x=readmission_counts.index,
    y=readmission_counts.values
)

plt.title("Overall Hospital Readmission Distribution")
plt.xlabel("Readmission Category")
plt.ylabel("Number of Encounters")
plt.tight_layout()
plt.show()


# %%
# 6.3 Readmission by age group

age_order = [
    "[0-10)", "[10-20)", "[20-30)", "[30-40)",
    "[40-50)", "[50-60)", "[60-70)", "[70-80)",
    "[80-90)", "[90-100)"
]

age_readmission = (
    df.groupby("age", observed=False)["readmission_30d"]
    .agg(["count", "mean"])
    .reset_index()
)

age_readmission["readmission_rate"] = (
    age_readmission["mean"] * 100
)

age_readmission["age"] = pd.Categorical(
    age_readmission["age"],
    categories=age_order,
    ordered=True
)

age_readmission = age_readmission.sort_values("age")

display(age_readmission)

plt.figure(figsize=(11, 5))

sns.barplot(
    data=age_readmission,
    x="age",
    y="readmission_rate"
)

plt.title("30-Day Readmission Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Readmission Rate (%)")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# %%
# 6.4 Readmission by gender and race

def plot_readmission_rate(data, column, title, top_n=None):

    summary = (
        data.groupby(column, dropna=False)["readmission_30d"]
        .agg(["count", "mean"])
        .reset_index()
    )

    summary["readmission_rate"] = summary["mean"] * 100

    if top_n is not None:
        summary = summary.nlargest(top_n, "count")

    display(summary)

    plt.figure(figsize=(10, 5))

    sns.barplot(
        data=summary,
        x=column,
        y="readmission_rate"
    )

    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("30-Day Readmission Rate (%)")
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()
    plt.show()


plot_readmission_rate(
    df,
    "gender",
    "30-Day Readmission Rate by Gender"
)

plot_readmission_rate(
    df,
    "race",
    "30-Day Readmission Rate by Race"
)


# %%
# 6.5 Admission type and discharge destination

plot_readmission_rate(
    df,
    "admission_type_id",
    "30-Day Readmission Rate by Admission Type"
)

plot_readmission_rate(
    df,
    "discharge_disposition_id",
    "30-Day Readmission Rate by Discharge Destination",
    top_n=12
)


# %%
# 6.6 Previous visits and medication count

plot_readmission_rate(
    df,
    "total_prior_visits",
    "30-Day Readmission Rate by Previous Healthcare Visits",
    top_n=15
)

plot_readmission_rate(
    df,
    "medication_count",
    "30-Day Readmission Rate by Medication Count",
    top_n=15
)


# %% [markdown]
# ## 7. Statistical Analysis
# 
# ### 7.1 Categorical Variable Association
# ### 7.2 Numerical Variable Comparison
# ### 7.3 Statistical Results Interpretation

# %%
# 7.1 Chi-square test for categorical variables

from scipy.stats import chi2_contingency

categorical_features = [
    "age",
    "gender",
    "race",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id"
]

chi_results = []

for column in categorical_features:

    contingency_table = pd.crosstab(
        df[column],
        df["readmission_30d"]
    )

    chi2, p_value, dof, expected = chi2_contingency(
        contingency_table
    )

    n = contingency_table.to_numpy().sum()

    minimum_dimension = min(contingency_table.shape) - 1

    cramers_v = (
        np.sqrt(chi2 / (n * minimum_dimension))
        if minimum_dimension > 0 else np.nan
    )

    chi_results.append({
        "Feature": column,
        "Chi_Square": chi2,
        "P_Value": p_value,
        "Cramers_V": cramers_v
    })

chi_results_df = pd.DataFrame(chi_results)

display(
    chi_results_df.sort_values("P_Value")
)


# %%
# 7.2 Mann–Whitney U test for numerical variables

from scipy.stats import mannwhitneyu

numerical_features = [
    "time_in_hospital",
    "num_lab_procedures",
    "num_procedures",
    "num_medications",
    "number_outpatient",
    "number_emergency",
    "number_inpatient",
    "number_diagnoses",
    "total_prior_visits",
    "medication_count"
]

numeric_results = []

for column in numerical_features:

    group_0 = df.loc[
        df["readmission_30d"] == 0, column
    ].dropna()

    group_1 = df.loc[
        df["readmission_30d"] == 1, column
    ].dropna()

    statistic, p_value = mannwhitneyu(
        group_0,
        group_1,
        alternative="two-sided"
    )

    numeric_results.append({
        "Feature": column,
        "Median_No_30d_Readmission": group_0.median(),
        "Median_30d_Readmission": group_1.median(),
        "P_Value": p_value
    })

numeric_results_df = pd.DataFrame(numeric_results)

display(
    numeric_results_df.sort_values("P_Value")
)



