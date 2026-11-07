# Healthcare Data Analytics & Data Quality Monitoring

## 1. Project Overview

**Dataset:** Diabetes 130-US Hospitals (1999–2008)  
**Source:** UCI Machine Learning Repository  
**Technologies:** Python, Pandas, NumPy, SQL (MySQL 8.0), Matplotlib and Seaborn.

**Objective:** Analyse healthcare encounter records, identify data quality issues, perform evidence-based data cleaning and generate meaningful analytical insights.

## 2. Initial Dataset Inspection

- Loaded the dataset successfully using Pandas.
- Confirmed the dataset contains 101,766 rows and 50 columns.
- Performed initial inspection using `shape`, `head()`, `info()` and `describe()`.
- Inspected column names, data types and sample records.
- Identified question mark (`?`) markers representing unavailable information.
- Confirmed that Pandas initially treated these markers as ordinary values rather than nulls.

## 3. Initial Missing-Value Findings

Calculated missing-value counts and percentages for the affected columns.

| Column | Missing count | Missing % |
|---|---:|---:|
| weight | 98,569 | 96.86% |
| medical_specialty | 49,949 | 49.08% |
| payer_code | 40,256 | 39.56% |
| race | 2,273 | 2.23% |
| diag_3 | 1,423 | 1.40% |
| diag_2 | 358 | 0.35% |
| diag_1 | 21 | 0.02% |

Also checked actual missing values recognised by Pandas and inspected the most common available values in each affected column.

## 4. Admission and Discharge Category Inspection

Investigated the following columns using frequency analysis:

- `admission_type_id`
- `discharge_disposition_id`
- `admission_source_id`

Reviewed `IDS_mapping.csv` to understand the meaning of the numerical category IDs.

Initial observations:

- Emergency admissions are the most frequent admission type.
- Emergency Room is the most frequent admission source.
- Discharge to home is the most frequent discharge category.
- These ID columns represent categories, not continuous numerical measurements.

## 5. Initial Data Quality Observations

- `weight` has the highest proportion of unavailable values (96.86%).
- `medical_specialty` and `payer_code` also have substantial missingness.
- Diagnosis fields have comparatively fewer missing values.
- Missing values will not automatically result in deleting rows or dropping columns.
- The original raw dataset has not been modified.
- Further investigation is required before choosing cleaning strategies.

## 6. Work Completed

- Loaded and inspected the raw CSV using Python and Pandas.
- Checked the dataset dimensions, column names and data types.
- Identified and quantified `?` missing-value markers.
- Checked actual null values recognised by Pandas.
- Inspected the available values in the seven columns containing `?`.
- Analysed the frequency distributions of admission type, discharge disposition and admission source.
- Used `IDS_mapping.csv` to interpret the admission and discharge category IDs.

## 7. Next Steps

1. Create a MySQL database named `healthcare_analytics`.
2. Import the original CSV into a raw SQL table without changing the source data.
3. Verify the imported row count and column structure.
4. Perform SQL-based missing-value checks and compare the results with Python.
5. Check duplicate encounter IDs and repeated patient identifiers.
6. Investigate distinct values, invalid values and inconsistent categories.
7. Define evidence-based cleaning and validation rules.
8. Continue with exploratory data analysis and healthcare-related insights.

## 8. Data Handling Principles

- Keep the original raw dataset unchanged.
- Preserve the original records during initial profiling.
- Investigate missing and unusual values before deciding how to handle them.
- Do not treat category IDs as continuous numerical values.
- Document cleaning decisions and validate the results using both Python and SQL.
- Remember that each row represents a hospital encounter; a patient may have multiple encounters.
- This is historical data from US hospitals (1999–2008), intended for learning and analysis rather than current clinical decision-making.
