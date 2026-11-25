# Healthcare Data Analytics --- Final Project Report

## 1. Executive Summary

This project analyses the Diabetes 130-US Hospitals dataset (1999--2008)
to investigate hospital encounter patterns, data quality and recorded
readmissions.

The workflow combines Python, MySQL and Power BI. Python was used for
data inspection, cleaning, feature engineering, exploratory data
analysis and statistical analysis. MySQL was used for structured data
management and SQL-based analysis. Power BI was used to create a
three-page interactive dashboard.

The original dataset contains 101,766 hospital encounters and 71,518
unique patients. Of the recorded encounters, 11.16% were labelled as
readmitted within 30 days.

The project is descriptive and analytical. It does not attempt to
predict individual patient outcomes or establish causal relationships.

## 2. Project Objectives

The main objectives were to:

1.  Understand the structure and quality of the healthcare dataset.
2.  Identify missing-value patterns and data inconsistencies.
3.  Examine patient and encounter-level characteristics.
4.  Analyse recorded readmission patterns using SQL and Python.
5.  Apply statistical methods to explore relationships in the data.
6.  Present important findings in an interactive Power BI dashboard.

## 3. Dataset Description

**Dataset:** Diabetes 130-US Hospitals (1999--2008)

**Source:** UCI Machine Learning Repository.

The dataset contains hospital encounter records, including:

-   Patient demographics.
-   Admission type and admission source.
-   Discharge disposition.
-   Primary, secondary and additional diagnosis codes.
-   Laboratory and medical procedures.
-   Medication information.
-   Readmission status.

The original data contains 101,766 rows and 50 columns.

Each row represents an encounter. A patient may appear in multiple rows
because they may have attended the hospital more than once.

## 4. Methodology

### 4.1 Data Inspection

The original CSV was loaded using Pandas.

The initial inspection covered:

-   Dataset dimensions.
-   Column names and data types.
-   Sample records.
-   Summary statistics.
-   Categorical distributions.
-   Missing-value markers.

The literal `?` marker was investigated separately from actual null
values.

Some of the largest missing-marker counts were:

  Column                 Count   Percentage
  ------------------- -------- ------------
  medical_specialty     49,949       49.08%
  payer_code            40,256       39.56%
  race                   2,273        2.23%
  diag_3                 1,423        1.40%
  diag_2                   358        0.35%
  diag_1                    21        0.02%

The `weight` field was set aside from the analysis because of its high
level of missingness.

### 4.2 SQL Database and Analysis

A MySQL 8.0 database named `healthcare_analytics` was created.

The original data was imported into `raw_diabetic_data`, with source
values initially stored as text to preserve the original representation.

The SQL workflow covered:

-   Database and table setup.
-   Data import.
-   Record and identifier inspection.
-   Patient encounter frequency.
-   Data-quality checks.
-   Admission, discharge and admission-source mapping tables.
-   Readmission analysis by admission type.
-   Readmission analysis by admission source.
-   Readmission analysis by discharge destination.
-   Diagnosis-code analysis.

The analysis was completed through the tenth SQL script.

### 4.3 Data Cleaning and Feature Engineering

A separate processed dataset was created rather than overwriting the
original source data.

The Python workflow included cleaning and validation checks, with
engineered features to support encounter-level analysis.

The four engineered features were:

  -----------------------------------------------------------------------
  Feature                             Description
  ----------------------------------- -----------------------------------
  `total_prior_visits`                Sum of outpatient, emergency and
                                      inpatient visit counts

  `medication_count`                  Count of diabetes medications
                                      recorded as Steady, Up or Down

  `medication_change_flag`            Indicates whether the medication
                                      change field is `Ch`

  `diabetes_medication_flag`          Indicates whether `diabetesMed` is
                                      `Yes`
  -----------------------------------------------------------------------

The original dataset and processed dataset were kept separate.

### 4.4 Exploratory and Statistical Analysis

The Python analysis explored:

-   Readmission distribution.
-   Patient and encounter characteristics.
-   Hospital activity.
-   Medication and procedure patterns.
-   Relationships between selected categorical and numerical variables.

Statistical methods used in the analysis included:

-   Chi-square tests for categorical associations.
-   Cramér's V for effect size.
-   Mann--Whitney U tests for comparisons between groups.
-   Rank-biserial effect size.
-   Benjamini--Hochberg false discovery rate correction for multiple
    testing.

Statistical significance should be considered alongside effect size,
sample size and practical relevance.

No predictive machine-learning models were retained in the final
project. The scope was kept focused on analytics and interpretation.

### 4.5 Power BI Dashboard

A three-page dashboard was created.

**Page 1 --- Healthcare Overview**

Provides a high-level view of encounter volume, unique patients,
readmission metrics and demographic distributions.

**Page 2 --- Readmission Analysis**

Explores readmission patterns across admission categories, discharge
destinations, age groups and previous visits.

**Page 3 --- Hospital Activity**

Examines length of stay, medication counts, laboratory procedures and
medical procedures.

The dashboard allows users to explore the dataset through interactive
visualisations and filters.

## 5. Results and Findings

### 5.1 Patient and Encounter Overview

  Metric                                  Result
  ------------------------------------ ---------
  Total encounters                       101,766
  Unique patients                         71,518
  Patients with multiple encounters       16,773
  Maximum encounters for one patient          40

The difference between the number of encounters and unique patients
demonstrates why patient-level and encounter-level metrics must be
distinguished.

### 5.2 Readmission Distribution

  Readmission category          Encounters   Percentage
  --------------------------- ------------ ------------
  No readmission                    54,864       53.91%
  Readmitted after 30 days          35,545       34.93%
  Readmitted within 30 days         11,357       11.16%

The majority of encounters were not followed by a recorded readmission.
Approximately one in nine encounters had a recorded readmission within
30 days.

### 5.3 Admission Type Analysis

  Admission type           Encounters   Within 30 days     Rate
  ---------------------- ------------ ---------------- --------
  Emergency                    53,990            6,221   11.52%
  Urgent                       18,480            2,066   11.18%
  Elective                     18,869            1,961   10.39%
  Not Available                 4,785              495   10.34%
  Mapping label `NULL`          5,291              586   11.08%

Emergency admissions had the highest 30-day readmission rate among the
larger recognised admission categories in this comparison.

The difference between Emergency and Urgent admissions was relatively
small, at 0.34 percentage points.

The categories Newborn and Trauma Center contained very few encounters,
so their percentages should not be interpreted as stable estimates.

### 5.4 Discharge Destination Analysis

  Discharge destination           Encounters   Within 30 days     Rate
  ----------------------------- ------------ ---------------- --------
  Home                                60,234            5,602    9.30%
  Home health                         12,902            1,638   12.70%
  Skilled nursing facility            13,954            2,046   14.66%
  Rehabilitation facility              1,993              552   27.70%
  Another short-term hospital          2,128              342   16.07%

The rehabilitation facility category had the highest 30-day readmission
rate among the destinations listed.

However, the number of encounters and the characteristics of patients
discharged to each destination differ. These results do not demonstrate
that the discharge destination caused readmission.

### 5.5 Data Quality

The analysis identified substantial missing-marker rates in some fields,
particularly `medical_specialty` and `payer_code`.

This reinforces the importance of:

-   Investigating missingness before removing records.
-   Preserving the distinction between unknown, unavailable and
    genuinely null values.
-   Documenting transformations.
-   Checking data consistency after cleaning.

## 6. Interpretation and Practical Implications

The findings demonstrate several useful analytical considerations.

**First, encounter counts are not patient counts.** Repeated encounters
need to be considered when interpreting healthcare activity.

**Second, readmission rates differ across categories.** Admission type
and discharge destination provide useful descriptive breakdowns, but
these differences need to be interpreted in the context of group size
and patient characteristics.

**Third, data quality influences analysis.** High missingness and coded
categorical fields can affect interpretation if they are not handled
carefully.

**Finally, visual reporting makes analysis more accessible.** The Power
BI dashboard provides a way to explore overall activity, readmission
patterns and hospital procedures without relying only on SQL query
outputs.

## 7. Limitations

1.  The data covers the historical period 1999--2008 and may not reflect
    current healthcare practice.
2.  The data is observational and does not establish causal
    relationships.
3.  Patients may have multiple encounters.
4.  Some columns contain substantial missingness.
5.  Mapping labels such as `NULL`, `Not Available` and `Not Mapped` need
    to be interpreted carefully.
6.  Diagnosis codes require an appropriate reference before assigning
    clinical descriptions.
7.  Small categories can produce unstable readmission percentages.
8.  The project is not a clinical decision-support system and should not
    be used to guide individual patient care.

## 8. Conclusion

This project delivered an end-to-end healthcare data analytics workflow
using Python, SQL and Power BI.

It covered raw data inspection, data-quality assessment, data cleaning,
feature engineering, SQL-based analysis, statistical testing and
interactive dashboard development.

The work demonstrated how healthcare encounter data can be transformed
into structured information and descriptive insights while maintaining
attention to data quality, statistical interpretation and responsible
use.

## 9. Future Improvements

Potential extensions include:

-   Adding a more detailed diagnosis-code reference.
-   Improving dashboard drill-through and documentation.
-   Comparing results across additional patient and encounter groups.
-   Building a separate, carefully evaluated readmission prediction
    project.
-   Developing a clinical document extraction pipeline using OCR, NLP
    and generative AI.

These would be separate extensions rather than claims about work
completed in this project.
