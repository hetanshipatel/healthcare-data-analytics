
# Healthcare Data Analytics: Diabetes 130-US Hospitals

## Project Overview

This project explores hospital encounter data from the Diabetes 130-US Hospitals dataset, covering clinical care records from 1999 to 2008.

The objective is to investigate patient encounters, data quality, admission patterns, diagnoses and hospital readmissions using SQL and Python.

The project follows a data analytics workflow, starting with raw data inspection and SQL-based analysis before progressing to Python data cleaning, exploratory data analysis and predictive modelling.

## Project Objectives

- Inspect and understand the structure of the healthcare dataset.
- Assess data quality, missing values and duplicate records.
- Explore patient encounter frequency and demographic distributions.
- Investigate readmission patterns within 30 days and after 30 days.
- Compare readmission rates across admission types and admission sources.
- Examine discharge destinations and their relationship with recorded readmissions.
- Explore primary, secondary and additional diagnosis codes.
- Prepare the dataset for further analysis and potential predictive modelling.

## Dataset

**Dataset:** Diabetes 130-US Hospitals for Years 1999–2008

The dataset contains hospital encounters involving patients with diabetes.

| Dataset characteristic | Value |
|---|---:|
| Total encounters | 101,766 |
| Unique patients | 71,518 |
| Original features | 50 |
| Time period | 1999–2008 |
| Duplicate encounter IDs detected | 0 |

Each row represents a hospital encounter, not necessarily a unique patient. A patient may therefore appear in multiple rows.

The project also uses `IDS_mapping.csv`, which provides descriptions for admission types, discharge dispositions and admission sources.

**Raw data is kept separate from processed project files.** The original dataset should remain unchanged.

## Tools and Technologies

- **SQL:** MySQL 8.0
- **Python:** Pandas and NumPy (for the Python analysis phase)
- **Jupyter Notebook:** Data inspection and analysis
- **VS Code:** Development environment
- **Git and GitHub:** Version control and project documentation

## Repository Structure

```text
healthcare-data-analytics/
│
├── data/
│   ├── raw/
│   │   ├── diabetic_data.csv
│   │   └── IDS_mapping.csv
│   │
│   └── processed/
│       ├── admission_type_mapping.csv
│       ├── discharge_disposition_mapping.csv
│       └── admission_source_mapping.csv
│
├── notebooks/
│   └── 01_raw_data_inspection.ipynb
│
├── reports/
│
├── sql/
│   ├── 01_database_setup.sql
│   ├── 02_create_raw_table.sql
│   ├── 03_load_raw_data.sql
│   ├── 04_raw_data_inspection.sql
│   ├── 05_data_quality_checks.sql
│   ├── 06_create_id_mapping_tables.sql
│   ├── 07_readmission_by_admission_type.sql
│   ├── 08_readmission_by_admission_source.sql
│   ├── 09_readmission_by_discharge_destination.sql
│   └── 10_diagnosis_analysis.sql
│
├── src/
│   └── prepare_id_mappings.py
│
├── PROJECT_NOTES.md
├── README.md
├── requirements.txt
└── .gitignore
```

## SQL Analysis

The SQL work is organised into ten scripts.

| Script | Analysis |
|---|---|
| 01 | Database setup |
| 02 | Creation of the raw data table |
| 03 | Raw dataset loading |
| 04 | Initial data inspection |
| 05 | Data quality checks |
| 06 | Admission and discharge mapping tables |
| 07 | Readmission by admission type |
| 08 | Readmission by admission source |
| 09 | Readmission by discharge destination |
| 10 | Diagnosis analysis |

The raw table contains 50 columns, initially stored as `VARCHAR(255)`.

## Key Findings

### 1. Patient and encounter analysis

- 101,766 total hospital encounters were present.
- 71,518 distinct patients were identified.
- 16,773 patients had multiple encounters.
- 54,745 patients had only one encounter.
- The highest number of encounters for one patient was 40.
- No duplicate encounter IDs were detected.

### 2. Readmission distribution

| Readmission category | Encounters | Percentage |
|---|---:|---:|
| No readmission (`NO`) | 54,864 | 53.91% |
| Readmitted after 30 days (`>30`) | 35,545 | 34.93% |
| Readmitted within 30 days (`<30`) | 11,357 | 11.16% |

### 3. Readmission by admission type

| Admission type | Encounters | 30-day readmission rate |
|---|---:|---:|
| Emergency | 53,990 | 11.52% |
| Urgent | 18,480 | 11.18% |
| Elective | 18,869 | 10.39% |
| Not Available | 4,785 | 10.34% |
| NULL mapping description | 5,291 | 11.08% |
| Newborn | 10 | 10.00% |
| Not Mapped | 320 | 8.44% |
| Trauma Center | 21 | 0.00% |

Emergency admissions had the highest 30-day readmission rate among the main admission categories. The difference between emergency and urgent admissions was relatively small.

Categories with very few encounters should not be compared as though their rates were equally reliable.

### 4. Readmission by admission source

The highest reported rates included:

| Admission source | Encounters | 30-day readmission rate |
|---|---:|---:|
| Transfer from hospital inpatient / same facility, separate claim | 12 | 16.67% |
| HMO Referral | 187 | 15.51% |
| Not Mapped | 161 | 13.66% |
| Court/Law Enforcement | 16 | 12.50% |
| Transfer from Skilled Nursing Facility | 855 | 11.81% |
| Emergency Room | 57,494 | 11.69% |
| Physician Referral | 29,565 | 10.59% |

The highest percentages include some categories with very small sample sizes. The Emergency Room category has a much larger number of encounters and is more useful for broad descriptive comparison.

### 5. Readmission by discharge destination

Some of the highest reported 30-day readmission rates were:

| Discharge destination | Encounters | 30-day readmission rate |
|---|---:|---:|
| Still patient / expected to return for outpatient services | 3 | 66.67% |
| Medicare approved swing bed | 63 | 44.44% |
| Admitted as inpatient to the same hospital | 21 | 42.86% |
| Psychiatric hospital | 139 | 36.69% |
| Rehabilitation facility | 1,993 | 27.70% |
| Another inpatient care institution | 1,184 | 20.86% |
| Another short-term hospital | 2,128 | 16.07% |
| Skilled Nursing Facility | 13,954 | 14.66% |
| Discharged to home | 60,234 | 9.30% |

Discharge destinations have very different encounter counts and meanings. In particular, expired and hospice categories should not be interpreted as ordinary discharge outcomes. Small categories also require caution.

### 6. Diagnosis analysis

The most frequent primary diagnosis codes included:

| Primary diagnosis code | Encounters |
|---|---:|
| 428 | 6,862 |
| 414 | 6,581 |
| 786 | 4,016 |
| 410 | 3,614 |
| 486 | 3,508 |
| 427 | 2,766 |
| 491 | 2,275 |
| 715 | 2,151 |
| 682 | 2,042 |
| 434 | 2,028 |

Diagnosis codes were analysed in three positions:

- Primary diagnosis (`diag_1`)
- Secondary diagnosis (`diag_2`)
- Additional secondary diagnosis (`diag_3`)

The diagnosis analysis also compared primary diagnosis codes with recorded 30-day readmissions, considering codes with at least 100 encounters.

The highest reported rates included:

| Primary diagnosis code | Encounters | 30-day readmission rate |
|---|---:|---:|
| V58 | 228 | 41.67% |
| 443 | 110 | 21.82% |
| 593 | 101 | 20.79% |
| 572 | 239 | 20.50% |
| 202 | 104 | 19.23% |
| 250.7 | 871 | 18.94% |
| 790 | 144 | 18.75% |
| 250.6 | 1,183 | 18.51% |

These are ICD-9 diagnosis codes. Clinical descriptions have not yet been added, so the results are reported using the original codes.

## Data Quality Observations

The SQL checks identified:

- No duplicate encounter IDs.
- No missing encounter or patient identifiers.
- Missing values represented by `?` in several columns.
- Weight had 98,569 missing markers and is not a focus of the current analysis.
- Medical specialty had 49,949 missing markers.
- Payer code had 40,256 missing markers.
- Race had 2,273 missing markers.
- `diag_1`, `diag_2` and `diag_3` had 21, 358 and 1,423 missing markers respectively.
- Three records had `Unknown/Invalid` gender.

The original raw data has been retained. Data cleaning and decisions about missing-value treatment will be documented separately in the Python phase.

## Limitations

- This is an observational, historical dataset covering 1999–2008.
- Each row represents an encounter rather than a unique patient.
- Readmission percentages are descriptive and do not establish causation.
- Some admission and discharge categories have very small sample sizes.
- Diagnosis codes have not yet been translated into clinical descriptions.
- Missing markers such as `?` need consistent handling during cleaning.
- Results should not be treated as current clinical guidance or used to make individual patient-care decisions.

## Next Steps

1. Continue Python data-quality analysis.
2. Standardise missing-value markers and inspect invalid values.
3. Investigate duplicate and inconsistent records.
4. Convert suitable columns to appropriate data types.
5. Create a cleaned dataset without modifying the raw source.
6. Perform exploratory data analysis and visualisation.
7. Investigate readmission patterns using Python.
8. Develop and evaluate a predictive model, if appropriate.
9. Document model limitations and interpret the results.

## Data Source

Diabetes 130-US Hospitals for Years 1999–2008.

The project uses the original encounter dataset and its associated ID mapping file. The raw dataset is not intended to be committed to the public Git repository.

---

*This project is for educational and portfolio purposes. It is not a clinical decision-support system.*
