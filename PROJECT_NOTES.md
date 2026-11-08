# Healthcare Data Analytics & Data Quality Monitoring

## 1. Project Overview

**Dataset:** Diabetes 130-US Hospitals (1999–2008)  
**Source:** UCI Machine Learning Repository  
**Technologies:** Python, Pandas, NumPy, SQL (MySQL 8.0), Matplotlib and Seaborn.

**Objective:** Analyse historical healthcare encounter records, identify data-quality issues, perform evidence-based data cleaning, and generate meaningful analytical insights.

**Important context:** Each row represents a hospital encounter, not necessarily a unique patient. A patient can appear in multiple rows because they may have multiple encounters.

## 2. Dataset and Initial Python Inspection

- Loaded the original CSV using Pandas.
- Confirmed that the dataset contains **101,766 rows and 50 columns**.
- Inspected the shape, column names, data types, sample records and descriptive statistics using `shape`, `head()`, `info()` and `describe()`.
- Identified question mark (`?`) values used as markers for unavailable information.
- Confirmed that Pandas initially reads `?` as an ordinary string rather than treating it as a missing value.
- Reviewed `IDS_mapping.csv` to understand the descriptions for admission type, discharge disposition and admission source codes.

## 3. Initial Missing-Value Findings

The following `?` marker counts were identified during the initial Python inspection:

| Column | Missing marker count | Missing % |
|---|---:|---:|
| `medical_specialty` | 49,949 | 49.08% |
| `payer_code` | 40,256 | 39.56% |
| `race` | 2,273 | 2.23% |
| `diag_3` | 1,423 | 1.40% |
| `diag_2` | 358 | 0.35% |
| `diag_1` | 21 | 0.02% |

These are counts of the literal `?` marker, not necessarily SQL `NULL` values. Actual nulls and empty strings should be checked separately.

## 4. Admission and Discharge Category Inspection

Investigated these categorical ID columns using frequency analysis:

- `admission_type_id`
- `discharge_disposition_id`
- `admission_source_id`

Reviewed `IDS_mapping.csv` to interpret the codes.

Initial observations:

- Emergency is the most frequent admission type.
- Emergency Room is the most frequent admission source.
- Discharge to home is the most frequent discharge category.
- These columns represent categories. Their numeric codes should not be interpreted as continuous measurements.
- Some mapping descriptions include labels such as `Not Available`, `Not Mapped` and `Unknown/Invalid`; these are descriptions associated with particular codes and should not automatically be treated as SQL nulls.

## 5. MySQL Database Setup and Raw Data Import

The following SQL setup work has been completed:

- Created the MySQL database `healthcare_analytics`.
- Selected the database using `USE healthcare_analytics`.
- Created the raw table `raw_diabetic_data` with 50 columns.
- Used `VARCHAR(255)` for the initial raw-table columns to preserve the imported values before applying type conversions or cleaning.
- Configured MySQL local-file loading and enabled `LOCAL INFILE` for the client and server.
- Created a `LOAD DATA LOCAL INFILE` script to import `data/raw/diabetic_data.csv`.
- Inspected a sample of the imported records and confirmed that the columns appeared aligned in the preview.

**Column-name handling:** Five medication-combination CSV headers contain hyphens. Their corresponding SQL column names use underscores:

- `glyburide-metformin` → `glyburide_metformin`
- `glipizide-metformin` → `glipizide_metformin`
- `glimepiride-pioglitazone` → `glimepiride_pioglitazone`
- `metformin-rosiglitazone` → `metformin_rosiglitazone`
- `metformin-pioglitazone` → `metformin_pioglitazone`

**Verification still required:** Confirm the final SQL row count against the Python dataset count of 101,766. Do not record the SQL import count as verified until the `COUNT(*)` result has been checked.

## 6. SQL Scripts Created

The `sql` folder contains the following setup and import scripts:

| File | Purpose |
|---|---|
| `01_database_setup.sql` | Creates and selects the `healthcare_analytics` database. |
| `02_create_raw_table.sql` | Creates the 50-column `raw_diabetic_data` raw table. |
| `03_load_raw_data.sql` | Loads the original CSV into the raw table using `LOAD DATA LOCAL INFILE`. |
| `04_raw_data_inspection.sql` | Collects initial record, encounter, patient, category and missing-value profile information. |

### SQL inspection work in `04_raw_data_inspection.sql`

The script includes queries to:

1. Count total records.
2. Count distinct encounter IDs.
3. Count distinct patient numbers.
4. Identify encounter IDs appearing more than once.
5. Find the minimum and maximum encounter ID values.
6. List patients with multiple encounters.
7. Calculate overall patient encounter statistics.
8. Show the distribution of encounters per patient.
9. Inspect gender distribution.
10. Inspect age-group distribution.
11. Inspect admission-type distribution.
12. Inspect readmission-label distribution and percentages.
13. Count `?` markers in selected columns.
14. Check selected columns for actual `NULL` or empty-string values.

The patient-level queries group records by `patient_nbr`. Repeated patient numbers are expected in encounter-level data and are not, by themselves, duplicate records.

**Results status:** The patient encounter queries have been run. Record the exact output values and final row-count/duplicate-check results here after reviewing the MySQL results. No numerical SQL findings are assumed in this document until verified.

## 7. Initial Data Quality Observations

- The raw data should remain unchanged during initial profiling.
- The literal `?` marker must be distinguished from actual SQL `NULL` and empty strings.
- Repeated `patient_nbr` values can represent multiple encounters for the same patient.
- Repeated `encounter_id` values require investigation because encounter IDs are expected to identify individual encounters.
- Admission and discharge ID columns are categorical.
- No rows or columns should be removed without a documented reason and an assessment of analytical impact.
- Cleaning and type conversion should take place in a separate staging or processed table, not by overwriting the raw source table.

## 8. Work Completed

- [x] Loaded and inspected the raw CSV using Python and Pandas.
- [x] Confirmed the dataset dimensions: 101,766 rows and 50 columns.
- [x] Inspected column names, data types and sample records.
- [x] Identified and quantified selected `?` missing-value markers.
- [x] Investigated admission type, discharge disposition and admission source frequencies.
- [x] Used `IDS_mapping.csv` to interpret the category IDs.
- [x] Created the MySQL `healthcare_analytics` database.
- [x] Created the `raw_diabetic_data` table.
- [x] Configured `LOCAL INFILE` and imported the CSV.
- [x] Inspected a sample of the imported SQL records.
- [x] Created SQL scripts for database setup, table creation, CSV loading and raw-data inspection.
- [x] Practised patient-level encounter counts using `GROUP BY`, `COUNT`, `HAVING`, `ORDER BY` and subqueries.

## 9. Next Steps

1. Confirm the SQL row count is 101,766 and compare it with the Python row count.
2. Review the outputs from `04_raw_data_inspection.sql`.
3. Confirm whether encounter IDs are unique and investigate any repeated IDs.
4. Compare SQL missing-marker counts with the Python findings.
5. Complete `05_data_quality_checks.sql` with systematic validation checks.
6. Investigate invalid values, unexpected categories and data-type issues.
7. Define and document cleaning rules before applying them to a separate staging table.
8. Continue with Python data cleaning and exploratory data analysis.
9. Build clear charts and summarise healthcare-related findings.
10. Update the README with the final project workflow, findings, limitations and instructions.

## 10. Data Handling and Interpretation Principles

- Preserve the original raw dataset and raw SQL table.
- Do not delete records or columns simply because they contain missing values.
- Distinguish missing markers (`?`), SQL `NULL` values and empty strings.
- Treat each row as a hospital encounter; patients may have multiple encounters.
- Validate transformations and compare important counts between Python and SQL.
- Document assumptions, cleaning decisions and limitations.
- This is historical data from US hospitals (1999–2008). It is suitable for learning and analytical portfolio work, not for current clinical decision-making or direct patient-care recommendations.
