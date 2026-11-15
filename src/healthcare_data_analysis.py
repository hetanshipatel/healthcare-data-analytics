# %% [markdown]
# # Healthcare Data Analytics – Cleaned Data Inspection
#
# This script loads the cleaned Diabetes 130-US Hospitals dataset and performs
# validation, exploratory data analysis, readmission analysis, and statistical
# testing. It does not train machine-learning models.

# %%
# 1. Import libraries

from pathlib import Path

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from IPython.display import display
from scipy.stats import chi2_contingency, mannwhitneyu


# %%
# 2. Locate the project folder and load the cleaned dataset

possible_roots = [Path.cwd(), Path.cwd().parent]

# When running this as src/healthcare_data_analysis.py, also check the
# project folder relative to this script.
try:
    possible_roots.append(Path(__file__).resolve().parents[1])
except NameError:
    pass

project_root = next(
    (
        path
        for path in possible_roots
        if (path / "data" / "processed" / "diabetic_data_cleaned.csv").exists()
    ),
    None,
)

if project_root is None:
    raise FileNotFoundError(
        "Could not find data/processed/diabetic_data_cleaned.csv. "
        "Run this script from the project folder, or check the dataset path."
    )

file_path = project_root / "data" / "processed" / "diabetic_data_cleaned.csv"
reports_dir = project_root / "reports"
reports_dir.mkdir(parents=True, exist_ok=True)

# Keep the original loaded data intact; convert individual columns when needed.
df = pd.read_csv(file_path)

print("Dataset loaded successfully!")
print("Dataset shape:", df.shape)
display(df.head())


def save_current_figure(filename):
    """Save the current chart to reports/ and display it."""
    output_path = reports_dir / filename
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches="tight")
    print(f"Chart saved: {output_path.relative_to(project_root)}")
    plt.show()
    plt.close()


# %% [markdown]
# ## 3. Dataset Validation

# %%

print("Rows:", df.shape[0])
print("Columns:", df.shape[1])
print("Total missing values:", df.isna().sum().sum())
print("Duplicate rows:", df.duplicated().sum())
print("Unique encounters:", df["encounter_id"].nunique())
print("Unique patients:", df["patient_nbr"].nunique())

engineered_features = [
    "total_prior_visits",
    "medication_count",
    "medication_change_flag",
    "diabetes_medication_flag",
]

missing_engineered = [col for col in engineered_features if col not in df.columns]
if missing_engineered:
    raise KeyError(f"Expected engineered features are missing: {missing_engineered}")

display(df[engineered_features].describe())

print("Total columns:", len(df.columns))
display(
    pd.DataFrame(
        {
            "Column_Name": df.columns,
            "Data_Type": df.dtypes.astype(str).values,
        }
    )
)


# %% [markdown]
# ## 4. Readmission Distribution

# %%

readmission_counts = df["readmitted"].value_counts(dropna=False)
readmission_percentage = (
    df["readmitted"].value_counts(normalize=True, dropna=False) * 100
).round(2)

print("Readmission counts:")
display(readmission_counts)
print("Readmission percentages:")
display(readmission_percentage)


# %% [markdown]
# ## 5. Exploratory Data Analysis
# ### 5.1 Patient Demographics

# %%

# A. Age distribution
age_order = [
    "[0-10)", "[10-20)", "[20-30)", "[30-40)", "[40-50)",
    "[50-60)", "[60-70)", "[70-80)", "[80-90)", "[90-100)",
]

plt.figure(figsize=(12, 6))
sns.countplot(data=df, x="age", order=age_order)
plt.title("Hospital Encounters by Age Group")
plt.xlabel("Age Group")
plt.ylabel("Number of Encounters")
plt.xticks(rotation=45)
save_current_figure("age_distribution.png")

# B. Gender distribution
gender_counts = df["gender"].value_counts()
display(gender_counts)

plt.figure(figsize=(7, 5))
sns.barplot(x=gender_counts.index, y=gender_counts.values)
plt.title("Hospital Encounters by Gender")
plt.xlabel("Gender")
plt.ylabel("Number of Encounters")
save_current_figure("gender_distribution.png")

# C. Race distribution
race_counts = df["race"].value_counts()
display(race_counts)

plt.figure(figsize=(10, 6))
sns.barplot(x=race_counts.values, y=race_counts.index)
plt.title("Hospital Encounters by Recorded Race")
plt.xlabel("Number of Encounters")
plt.ylabel("Race")
save_current_figure("race_distribution.png")


# %% [markdown]
# ## 6. Hospital Activity Analysis

# %%

# 6.1 Length of hospital stay
# Convert to numeric safely in case the CSV stores this column as text.
df["time_in_hospital"] = pd.to_numeric(df["time_in_hospital"], errors="coerce")
print("Hospital stay summary:")
display(df["time_in_hospital"].describe())

plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="time_in_hospital", bins=14, kde=True)
plt.title("Distribution of Hospital Stay Duration")
plt.xlabel("Days in Hospital")
plt.ylabel("Number of Encounters")
save_current_figure("hospital_stay_distribution.png")

# 6.2 Number of laboratory procedures
df["num_lab_procedures"] = pd.to_numeric(df["num_lab_procedures"], errors="coerce")
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="num_lab_procedures", bins=30, kde=True)
plt.title("Distribution of Laboratory Procedures")
plt.xlabel("Number of Lab Procedures")
plt.ylabel("Number of Encounters")
save_current_figure("lab_procedures_distribution.png")
display(df["num_lab_procedures"].describe())

# 6.3 Number of medical procedures
df["num_procedures"] = pd.to_numeric(df["num_procedures"], errors="coerce")
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="num_procedures", bins=15, discrete=True)
plt.title("Distribution of Medical Procedures")
plt.xlabel("Number of Procedures")
plt.ylabel("Number of Encounters")
save_current_figure("medical_procedures_distribution.png")

# 6.4 Number of medications
df["num_medications"] = pd.to_numeric(df["num_medications"], errors="coerce")
plt.figure(figsize=(10, 5))
sns.histplot(data=df, x="num_medications", bins=30, kde=True)
plt.title("Distribution of Medications per Encounter")
plt.xlabel("Number of Medications")
plt.ylabel("Number of Encounters")
save_current_figure("medications_distribution.png")

# 6.5 Previous hospital visits
df["total_prior_visits"] = pd.to_numeric(df["total_prior_visits"], errors="coerce")
plt.figure(figsize=(10, 5))
sns.countplot(data=df, x="total_prior_visits")
plt.title("Previous Healthcare Visits per Encounter")
plt.xlabel("Total Previous Visits")
plt.ylabel("Number of Encounters")
plt.xticks(rotation=45)
save_current_figure("previous_visits_distribution.png")

# 6.6 Compare hospital stay with readmission
plt.figure(figsize=(10, 6))
sns.boxplot(
    data=df,
    x="readmitted",
    y="time_in_hospital",
    order=["NO", ">30", "<30"],
)
plt.title("Hospital Stay Duration by Readmission Category")
plt.xlabel("Readmission Category")
plt.ylabel("Days in Hospital")
save_current_figure("hospital_stay_by_readmission.png")


# %% [markdown]
# ## 7. Readmission Analysis
# ### 7.1 Create the 30-day readmission indicator
# ### 7.2 Overall readmission distribution
# ### 7.3 Readmission by age group
# ### 7.4 Readmission by gender and race
# ### 7.5 Admission type and discharge destination
# ### 7.6 Previous visits and medication count

# %%

# A value of 1 means readmitted within 30 days (<30).
# A value of 0 means not readmitted within 30 days (NO or >30).
df["readmission_30d"] = df["readmitted"].eq("<30").astype(int)

print("30-day readmission indicator created.")
display(df["readmission_30d"].value_counts().rename(index={0: "Not within 30 days", 1: "Within 30 days"}))
display(
    (df["readmission_30d"].value_counts(normalize=True) * 100)
    .rename(index={0: "Not within 30 days", 1: "Within 30 days"})
    .round(2)
)

# 7.2 Overall readmission distribution
readmission_counts = df["readmitted"].value_counts()
plt.figure(figsize=(8, 5))
sns.barplot(x=readmission_counts.index, y=readmission_counts.values)
plt.title("Overall Hospital Readmission Distribution")
plt.xlabel("Readmission Category")
plt.ylabel("Number of Encounters")
save_current_figure("overall_readmission_distribution.png")

# 7.3 Readmission by age group
age_readmission = (
    df.groupby("age", observed=False)["readmission_30d"]
    .agg(encounter_count="count", readmission_rate="mean")
    .reset_index()
)
age_readmission["readmission_rate"] *= 100
age_readmission["age"] = pd.Categorical(
    age_readmission["age"], categories=age_order, ordered=True
)
age_readmission = age_readmission.sort_values("age")
display(age_readmission)
age_readmission.to_csv(reports_dir / "readmission_by_age.csv", index=False)

plt.figure(figsize=(11, 5))
sns.barplot(data=age_readmission, x="age", y="readmission_rate")
plt.title("30-Day Readmission Rate by Age Group")
plt.xlabel("Age Group")
plt.ylabel("30-Day Readmission Rate (%)")
plt.xticks(rotation=45)
save_current_figure("readmission_by_age.png")

# Helper function for readmission rates by category.
def plot_readmission_rate(data, column, title, filename, top_n=None):
    """Display, save and return encounter counts and 30-day readmission rates."""
    summary = (
        data.groupby(column, dropna=False, observed=False)["readmission_30d"]
        .agg(encounter_count="count", readmission_rate="mean")
        .reset_index()
    )
    summary["readmission_rate"] *= 100

    if top_n is not None:
        summary = summary.nlargest(top_n, "encounter_count")

    display(summary)
    summary.to_csv(reports_dir / f"{filename.replace('.png', '.csv')}", index=False)

    plt.figure(figsize=(10, 5))
    sns.barplot(data=summary, x=column, y="readmission_rate")
    plt.title(title)
    plt.xlabel(column)
    plt.ylabel("30-Day Readmission Rate (%)")
    plt.xticks(rotation=45, ha="right")
    save_current_figure(filename)
    return summary


# 7.4 Readmission by gender and race
gender_readmission = plot_readmission_rate(
    df, "gender", "30-Day Readmission Rate by Gender", "readmission_by_gender.png"
)
race_readmission = plot_readmission_rate(
    df, "race", "30-Day Readmission Rate by Race", "readmission_by_race.png"
)

# 7.5 Admission type and discharge destination
admission_type_readmission = plot_readmission_rate(
    df,
    "admission_type_id",
    "30-Day Readmission Rate by Admission Type",
    "readmission_by_admission_type.png",
)
discharge_readmission = plot_readmission_rate(
    df,
    "discharge_disposition_id",
    "30-Day Readmission Rate by Discharge Destination (Top 12 by Count)",
    "readmission_by_discharge_destination.png",
    top_n=12,
)

# 7.6 Previous visits and medication count
prior_visits_readmission = plot_readmission_rate(
    df,
    "total_prior_visits",
    "30-Day Readmission Rate by Previous Healthcare Visits (Top 15 by Count)",
    "readmission_by_prior_visits.png",
    top_n=15,
)
medication_count_readmission = plot_readmission_rate(
    df,
    "medication_count",
    "30-Day Readmission Rate by Medication Count (Top 15 by Count)",
    "readmission_by_medication_count.png",
    top_n=15,
)


# %% [markdown]
# ## 8. Statistical Analysis
# ### 8.1 Chi-square tests for categorical variables
# ### 8.2 Mann–Whitney U tests for numerical variables
# ### 8.3 Multiple-testing correction and effect sizes
#
# P-values indicate evidence against the null hypothesis. Effect sizes help
# describe the strength and direction of an association. Statistical
# significance does not establish causation.

# %%

# Benjamini–Hochberg false-discovery-rate adjustment, implemented here to
# avoid requiring an additional package such as statsmodels.
def benjamini_hochberg(p_values):
    """Return Benjamini-Hochberg adjusted p-values in original input order."""
    p_values = np.asarray(p_values, dtype=float)
    adjusted = np.full(p_values.shape, np.nan, dtype=float)
    valid_mask = np.isfinite(p_values)
    valid_p = p_values[valid_mask]

    if valid_p.size == 0:
        return adjusted

    order = np.argsort(valid_p)
    ranked_p = valid_p[order]
    n_tests = len(ranked_p)
    adjusted_ranked = ranked_p * n_tests / np.arange(1, n_tests + 1)
    adjusted_ranked = np.minimum.accumulate(adjusted_ranked[::-1])[::-1]
    adjusted_ranked = np.clip(adjusted_ranked, 0, 1)

    restored = np.empty(n_tests, dtype=float)
    restored[order] = adjusted_ranked
    adjusted[valid_mask] = restored
    return adjusted


# 8.1 Chi-square tests for categorical variables
categorical_features = [
    "age",
    "gender",
    "race",
    "admission_type_id",
    "discharge_disposition_id",
    "admission_source_id",
]

chi_results = []

for column in categorical_features:
    contingency_table = pd.crosstab(df[column], df["readmission_30d"])

    # A valid chi-square test needs at least two rows and two columns.
    if contingency_table.shape[0] < 2 or contingency_table.shape[1] < 2:
        print(f"Skipping {column}: not enough categories for a chi-square test.")
        continue

    chi2, p_value, dof, expected = chi2_contingency(contingency_table)
    n = contingency_table.to_numpy().sum()
    min_dimension = min(contingency_table.shape) - 1

    cramers_v = (
        np.sqrt(chi2 / (n * min_dimension)) if min_dimension > 0 else np.nan
    )

    chi_results.append(
        {
            "Feature": column,
            "Chi_Square": chi2,
            "Degrees_of_Freedom": dof,
            "P_Value": p_value,
            "Cramers_V": cramers_v,
            "Minimum_Expected_Count": expected.min(),
            "Expected_Cells_Below_5_Pct": (expected < 5).mean() * 100,
        }
    )

chi_results_df = pd.DataFrame(chi_results)
if not chi_results_df.empty:
    chi_results_df["Adjusted_P_Value"] = benjamini_hochberg(
        chi_results_df["P_Value"]
    )
    chi_results_df["Significant_After_FDR_0_05"] = (
        chi_results_df["Adjusted_P_Value"] < 0.05
    )
    chi_results_df = chi_results_df.sort_values("Adjusted_P_Value")
    display(chi_results_df)
    chi_results_df.to_csv(reports_dir / "chi_square_results.csv", index=False)

# 8.2 Mann–Whitney U tests for numerical variables
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
    "medication_count",
]

numeric_results = []

for column in numerical_features:
    # Ensure each tested feature is numeric.
    numeric_values = pd.to_numeric(df[column], errors="coerce")
    group_0 = numeric_values[df["readmission_30d"] == 0].dropna()
    group_1 = numeric_values[df["readmission_30d"] == 1].dropna()

    if group_0.empty or group_1.empty:
        print(f"Skipping {column}: one of the comparison groups is empty.")
        continue

    statistic, p_value = mannwhitneyu(
        group_0, group_1, alternative="two-sided", method="auto"
    )

    # Rank-biserial correlation: positive values mean group 0 tends to have
    # larger values; negative values mean group 1 tends to have larger values.
    denominator = len(group_0) * len(group_1)
    rank_biserial = (2 * statistic / denominator) - 1

    numeric_results.append(
        {
            "Feature": column,
            "Group_0_Count": len(group_0),
            "Group_1_Count": len(group_1),
            "Median_Not_Within_30_Days": group_0.median(),
            "Median_Within_30_Days": group_1.median(),
            "Mann_Whitney_U": statistic,
            "P_Value": p_value,
            "Rank_Biserial_Correlation": rank_biserial,
            "Absolute_Effect_Size": abs(rank_biserial),
        }
    )

numeric_results_df = pd.DataFrame(numeric_results)
if not numeric_results_df.empty:
    numeric_results_df["Adjusted_P_Value"] = benjamini_hochberg(
        numeric_results_df["P_Value"]
    )
    numeric_results_df["Significant_After_FDR_0_05"] = (
        numeric_results_df["Adjusted_P_Value"] < 0.05
    )
    numeric_results_df = numeric_results_df.sort_values("Adjusted_P_Value")
    display(numeric_results_df)
    numeric_results_df.to_csv(reports_dir / "mann_whitney_results.csv", index=False)


# %% [markdown]
# ## 9. Save Key Analysis Tables
#
# The following CSV files are written to reports/ for later reporting and
# Power BI preparation. The cleaned source dataset is not modified.

# %%

# Save readmission distribution
readmission_summary = pd.DataFrame(
    {
        "Readmission_Category": readmission_counts.index.astype(str),
        "Encounter_Count": readmission_counts.values,
        "Percentage": [
            (count / len(df)) * 100 for count in readmission_counts.values
        ],
    }
)
readmission_summary.to_csv(reports_dir / "readmission_distribution.csv", index=False)

print("\nAnalysis completed.")
print(f"Charts and analysis tables saved in: {reports_dir}")
print("No machine-learning models were trained in this analysis script.")
