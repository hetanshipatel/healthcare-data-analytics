# Healthcare Data Analytics & Data Quality Monitoring

## 1. Project Overview

**Dataset:** Diabetes 130-US Hospitals (1999–2008)

**Source:** UCI Machine Learning Repository

**Technologies:** Python, Pandas, NumPy, SQL (MySQL 8.0), Matplotlib and Seaborn.

**Objective:** Analyse healthcare encounter records, identify data quality issues, perform data cleaning and generate meaningful analytical insights.

## 2. Initial Dataset Inspection

- Dataset loaded successfully using Pandas.
- Initial inspection performed using `shape`, `head()`, `info()` and `describe()`.
- Identified question mark (`?`) markers representing unavailable information.
- Pandas initially treated these markers as ordinary values rather than nulls.

## 3. Initial Missing-Value Findings

| Column | Missing count | Missing % |
|---|---:|---:|
| weight | 98,569 | 96.86% |
| medical_specialty | 49,949 | 49.08% |
| payer_code | 40,256 | 39.56% |
| race | 2,273 | 2.23% |
| diag_3 | 1,423 | 1.40% |
| diag_2 | 358 | 0.35% |
| diag_1 | 21 | 0.02% |

## 4. Initial Observations

- Weight has the highest proportion of unavailable values.
- Medical specialty and payer code also have substantial missingness.
- Diagnosis fields have comparatively fewer missing values.
- Further investigation is required before deciding on cleaning strategies.

## 5. Pending Investigation

- Inspect unique and distinct values.
- Check duplicate encounters.
- Investigate data types and inconsistent categories.
- Load raw data into MySQL.
- Perform SQL-based data quality checks.
- Establish cleaning and validation rules.