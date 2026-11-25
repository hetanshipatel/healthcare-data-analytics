# Healthcare Data Analytics --- Hospital Readmission Analysis

## Project Overview

This project explores hospital encounters and recorded readmissions
using the **Diabetes 130-US Hospitals (1999--2008)** dataset.

The objective was to investigate data quality, understand patient
encounter patterns, analyse readmission trends and communicate findings
through Python, SQL and an interactive Power BI dashboard.

The project follows a data analytics workflow from raw data inspection
and cleaning through SQL analysis, statistical exploration and visual
reporting.

## Business Questions

-   What data-quality issues exist in the original dataset?
-   How many hospital encounters and unique patients are represented?
-   How does readmission vary across admission types and discharge
    destinations?
-   Which diagnosis codes occur most frequently?
-   How do patient demographics and hospital activity relate
    descriptively to readmission?
-   What insights can be communicated through an interactive dashboard?

## Dataset

**Source:** UCI Machine Learning Repository --- Diabetes 130-US
Hospitals (1999--2008).

-   Original dataset: 101,766 encounters and 50 columns.
-   Each row represents a hospital encounter.
-   Patients may have multiple encounters.
-   The dataset includes demographics, admission details, diagnoses,
    medications, procedures and readmission status.

The dataset is historical and is used for educational analysis. It is
not intended for clinical decision-making.

## Technologies

  Technology               Purpose
  ------------------------ ------------------------------------------------------------
  Python                   Data cleaning, exploration and statistical analysis
  Pandas and NumPy         Data manipulation
  Matplotlib and Seaborn   Data visualisation
  MySQL 8.0                Data storage and SQL analysis
  SQL                      Data quality checks, aggregations and readmission analysis
  Power BI                 Interactive dashboard and reporting
  Git and GitHub           Version control and project documentation

## Project Structure

``` text
healthcare-data-analytics/
├── data/
│   ├── raw/
│   └── processed/
├── notebooks/
│   ├── 01_raw_data_inspection.ipynb
│   └── 02_cleaned_data_inspection.ipynb
├── reports/
│   ├── FINAL_PROJECT_REPORT.md
│   ├── healthcare_analytics_dashboard.pbix
│   └── images/
├── sql/
├── src/
│   └── healthcare_data_analysis.py
├── .gitignore
├── PROJECT_NOTES.md
├── README.md
└── requirements.txt
```

Raw and processed patient-level datasets should remain local and must
not be committed to a public repository. The Power BI file should also
be checked for embedded patient-level data before sharing.

## Project Workflow

### 1. Data Inspection and Quality Assessment

-   Inspected the original dataset using Python and Pandas.
-   Reviewed dimensions, column names, data types and category
    distributions.
-   Identified missing-value markers represented by `?`.
-   Examined missingness across important columns.
-   Preserved the original raw data separately from the cleaned dataset.

Selected literal `?` marker counts:

  Column                 Count   Percentage
  ------------------- -------- ------------
  medical_specialty     49,949       49.08%
  payer_code            40,256       39.56%
  race                   2,273        2.23%
  diag_3                 1,423        1.40%
  diag_2                   358        0.35%
  diag_1                    21        0.02%

These counts represent literal `?` values, not confirmed SQL NULL
counts.

### 2. SQL Analysis

Used MySQL 8.0 to:

-   Create the `healthcare_analytics` database and `raw_diabetic_data`
    table.
-   Import and inspect the original dataset.
-   Analyse encounter and patient identifiers.
-   Examine repeated patient encounters.
-   Investigate data quality and categorical distributions.
-   Prepare mapping tables for admission type, admission source and
    discharge destination.
-   Analyse readmission patterns by admission type, admission source,
    discharge destination and diagnosis.

SQL analysis was completed through the tenth analysis script.

### 3. Python Analysis

Used Python for:

-   Data cleaning and validation.
-   Feature engineering.
-   Exploratory data analysis.
-   Readmission distribution analysis.
-   Hospital activity analysis.
-   Statistical association testing.
-   Effect-size calculations and multiple-testing correction.

Engineered features included:

-   `total_prior_visits`
-   `medication_count`
-   `medication_change_flag`
-   `diabetes_medication_flag`

Statistical methods included Chi-square tests, Cramér's V, Mann--Whitney
U tests, rank-biserial effect size and Benjamini--Hochberg false
discovery rate correction.

No predictive machine-learning model was included in the final project.
The focus remained on descriptive and statistical analysis.

### 4. Power BI Dashboard

Created a three-page Power BI report:

**Page 1 --- Healthcare Overview** - Overall encounter and patient
metrics. - Readmission overview. - Demographic and encounter
distributions.

**Page 2 --- Readmission Analysis** - Readmission patterns across
patient and admission categories. - Comparisons by admission and
discharge information. - Previous-visit analysis.

**Page 3 --- Hospital Activity** - Length of stay. - Medication usage. -
Laboratory and medical procedure activity.

The dashboard is saved as a Power BI `.pbix` file. Dashboard screenshots
are stored in the `reports/` folder.

## Key Findings

### Dataset and Patient Encounters

-   Total encounters: **101,766**
-   Unique patients: **71,518**
-   Patients with multiple encounters: **16,773**
-   Maximum recorded encounters for one patient: **40**

This confirms that encounter-level records should not be interpreted as
unique individual patients.

### Readmission Distribution

  Readmission category          Encounters   Percentage
  --------------------------- ------------ ------------
  No readmission                    54,864       53.91%
  Readmitted after 30 days          35,545       34.93%
  Readmitted within 30 days         11,357       11.16%

### Readmission by Admission Type

  Admission type           Encounters   Within 30 days     Rate
  ---------------------- ------------ ---------------- --------
  Emergency                    53,990            6,221   11.52%
  Urgent                       18,480            2,066   11.18%
  Elective                     18,869            1,961   10.39%
  Not Available                 4,785              495   10.34%
  Mapping label `NULL`          5,291              586   11.08%

Emergency admissions had the highest 30-day rate among the larger
recognised categories shown. The difference between Emergency and Urgent
was 0.34 percentage points. Small categories such as Newborn and Trauma
Center should not be over-interpreted.

The `NULL` value above is a mapping description and is not proof of SQL
NULL values.

### Readmission by Discharge Destination

  Discharge destination           Encounters   Within 30 days     Rate
  ----------------------------- ------------ ---------------- --------
  Home                                60,234            5,602    9.30%
  Home health                         12,902            1,638   12.70%
  Skilled nursing facility            13,954            2,046   14.66%
  Rehabilitation facility              1,993              552   27.70%
  Another short-term hospital          2,128              342   16.07%

These are descriptive comparisons. Differences may reflect patient and
encounter characteristics and should not be interpreted as causal
effects of discharge destination.

## Dashboard Screenshots

Keep the exported screenshots in `reports/` or `reports/images/`. Update
these paths to match the filenames you actually saved.

-   Healthcare Overview: `reports/healthcare_overview.png`
-   Readmission Analysis: `reports/readmission_analysis.png`
-   Hospital Activity: `reports/hospital_activity.png`

## Limitations

-   The dataset covers historical hospital encounters from 1999--2008.
-   Multiple encounters can belong to the same patient.
-   Missing-value markers, empty strings and SQL NULL values are not
    interchangeable.
-   Admission and discharge identifiers are categorical codes.
-   Diagnosis codes require a reliable reference before assigning
    clinical descriptions.
-   Small categories may produce unstable percentages.
-   Observational analysis does not establish causality.
-   This project is not intended for patient-care decisions.

## Reproducibility

1.  Download the dataset from the UCI Machine Learning Repository.
2.  Place the original files in the local `data/raw/` folder.
3.  Install the Python dependencies listed in `requirements.txt`.
4.  Run the notebooks in the documented order.
5.  Configure MySQL 8.0 and run the SQL scripts in numerical order.
6.  Run the Python analysis script.
7.  Open the Power BI report in Power BI Desktop and update the local
    data source path if necessary.

Local file paths and database settings may need adjustment on another
computer.

## Final Outcome

The project combines Python, SQL and Power BI to demonstrate a
healthcare data analytics workflow, from data quality assessment and
transformation to statistical analysis and interactive reporting.

**Focus:** Data quality, exploratory analysis, SQL, statistical testing,
healthcare analytics and data visualisation.
