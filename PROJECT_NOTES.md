
# Healthcare Data Analytics — Project Notes

## 1. Project Information

**Project:** Healthcare Data Analytics — Diabetes 130-US Hospitals

**Dataset:** Diabetes 130-US Hospitals for Years 1999–2008

**Database:** `healthcare_analytics`

**Raw table:** `raw_diabetic_data`

**SQL environment:** MySQL 8.0 Command Line Client

**Development environment:** VS Code

**Current phase:** SQL analysis completed; Python data-quality and cleaning phase pending.

### Project aim

To explore hospital encounter data involving patients with diabetes, identify data-quality issues, investigate readmission patterns and prepare the dataset for further exploratory analysis and predictive modelling.

The project uses SQL for structured data inspection and analysis, followed by Python for more detailed data preparation and analysis.

---

## 2. Dataset Overview

The dataset contains 101,766 hospital encounters and 50 original features.

| Metric | Result |
|---|---:|
| Total encounters | 101,766 |
| Unique patients | 71,518 |
| Distinct encounter IDs | 101,766 |
| Duplicate encounter IDs | 0 |
| First encounter ID in the dataset | 12,522 |
| Last encounter ID in the dataset | 443,867,222 |
| Original features | 50 |

**Important:** Each row represents a hospital encounter. It does not necessarily represent a different patient. Patients can have multiple encounters.

The original raw data is stored separately and should not be overwritten during data cleaning.

### Dataset files

- `diabetic_data.csv` — main hospital encounter dataset.
- `IDS_mapping.csv` — descriptions for admission types, discharge dispositions and admission sources.

---

## 3. Project Structure

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

---

## 4. Python Work Completed Before SQL

The notebook `01_raw_data_inspection.ipynb` was used to inspect the raw CSV dataset.

Work completed:

- Loaded the raw dataset using Pandas.
- Checked the dataset shape and column names.
- Inspected data types and sample records.
- Reviewed categorical columns and their distributions.
- Investigated the `?` missing-value marker.
- Inspected the ID mapping file.
- Reviewed admission-type categories.
- Identified diagnosis fields as categorical ICD-9 codes.

### Missing-value markers identified in Python

| Column | Missing markers (`?`) | Percentage |
|---|---:|---:|
| weight | 98,569 | 96.86% |
| medical_specialty | 49,949 | 49.08% |
| payer_code | 40,256 | 39.56% |
| race | 2,273 | 2.23% |
| diag_3 | 1,423 | 1.40% |
| diag_2 | 358 | 0.35% |
| diag_1 | 21 | 0.02% |

Weight is not a focus of the current analysis because of its very high missingness.

The `?` marker must be handled explicitly during Python cleaning. It is not automatically equivalent to a Pandas missing value unless it is converted.

---

## 5. MySQL Database Setup

The MySQL database is named:

```sql
healthcare_analytics
```

The primary encounter table is:

```sql
raw_diabetic_data
```

The raw table contains 50 columns, initially defined as:

```sql
VARCHAR(255)
```

This allowed the original values to be imported without immediately converting fields to numeric or date types.

The five medication column names containing hyphens in the CSV were represented with underscores in the MySQL table:

| Original CSV name | MySQL column name |
|---|---|
| glyburide-metformin | glyburide_metformin |
| glipizide-metformin | glipizide_metformin |
| glimepiride-pioglitazone | glimepiride_pioglitazone |
| metformin-rosiglitazone | metformin_rosiglitazone |
| metformin-pioglitazone | metformin_pioglitazone |

### Mapping tables

Three mapping tables were available in the database:

| Table | Records |
|---|---:|
| admission_type_mapping | 8 |
| discharge_disposition_mapping | 30 |
| admission_source_mapping | 25 |

These tables translate numeric IDs into readable descriptions and were used in the readmission analysis.

### Import execution note

During the SQL rerun, MySQL returned:

```text
ERROR 3948 (42000):
Loading local data is disabled;
this must be enabled on both the client and server sides
```

This occurred in:

- `03_load_raw_data.sql`
- `06_create_id_mapping_tables.sql`

However, subsequent queries confirmed that the encounter table contained 101,766 records and that the three mapping tables contained 8, 30 and 25 records respectively.

Therefore, the data and mappings were present at the time of analysis, but the local import commands did not successfully run during that particular rerun.

Do not assume that a failed import command has refreshed a table. Before future imports, verify the client and server `local_infile` settings and check the resulting row counts.

---

## 6. SQL Analysis

Ten SQL scripts were created for the project.

| Script | Purpose |
|---|---|
| 01_database_setup.sql | Database setup |
| 02_create_raw_table.sql | Create raw encounter table |
| 03_load_raw_data.sql | Load encounter CSV |
| 04_raw_data_inspection.sql | Initial inspection and distributions |
| 05_data_quality_checks.sql | Data quality and missing-value checks |
| 06_create_id_mapping_tables.sql | Create and populate ID mapping tables |
| 07_readmission_by_admission_type.sql | Compare admission types |
| 08_readmission_by_admission_source.sql | Compare admission sources |
| 09_readmission_by_discharge_destination.sql | Compare discharge destinations |
| 10_diagnosis_analysis.sql | Analyse diagnosis codes and readmissions |

### 6.1 Raw data inspection

The following checks were performed:

- Total record count.
- Distinct encounter IDs.
- Distinct patient numbers.
- Minimum and maximum encounter IDs.
- Patients with multiple encounters.
- Distribution of encounters per patient.
- Gender distribution.
- Age distribution.
- Admission-type distribution.
- Readmission distribution.
- Missing-value marker counts.

### 6.2 Patient encounter analysis

| Metric | Result |
|---|---:|
| Unique patients | 71,518 |
| Patients with one encounter | 54,745 |
| Patients with multiple encounters | 16,773 |
| Maximum encounters for one patient | 40 |

Approximately 23.45% of the unique patients had multiple encounters.

The encounter distribution was:

| Encounters per patient | Number of patients |
|---:|---:|
| 1 | 54,745 |
| 2 | 10,434 |
| 3 | 3,328 |
| 4 | 1,421 |
| 5 | 717 |
| 6 | 346 |
| 7 | 207 |
| 8 | 111 |
| 9 | 70 |
| 10 | 42 |
| 11 | 20 |
| 12 | 19 |
| 13 | 14 |
| 14 | 5 |
| 15 | 9 |
| 16 | 4 |
| 17 | 3 |
| 18 | 6 |
| 19 | 3 |
| 20 | 6 |
| 21 | 1 |
| 22 | 2 |
| 23 | 3 |
| 28 | 1 |
| 40 | 1 |

This confirms that encounter-level and patient-level analysis must be distinguished.

### 6.3 Gender distribution

| Gender | Encounters |
|---|---:|
| Female | 54,708 |
| Male | 47,055 |
| Unknown/Invalid | 3 |

### 6.4 Age distribution

| Age group | Encounters |
|---|---:|
| [0-10) | 161 |
| [10-20) | 691 |
| [20-30) | 1,657 |
| [30-40) | 3,775 |
| [40-50) | 9,685 |
| [50-60) | 17,256 |
| [60-70) | 22,483 |
| [70-80) | 26,068 |
| [80-90) | 17,197 |
| [90-100) | 2,793 |

The 70–80 age group had the highest number of encounters.

---

## 7. Data Quality Results

The SQL quality checks identified:

| Check | Result |
|---|---:|
| Total records | 101,766 |
| Duplicate encounter IDs | 0 |
| Records with missing identifiers | 0 |
| Missing weight markers | 98,569 |
| Missing race markers | 2,273 |
| Missing payer-code markers | 40,256 |
| Missing medical-specialty markers | 49,949 |
| Missing primary diagnosis markers | 21 |
| Missing secondary diagnosis markers | 358 |
| Missing additional diagnosis markers | 1,423 |

The SQL checks also returned zero for NULL-or-empty values in the six inspected columns. This is consistent with the missing values being represented by `?` rather than SQL `NULL` or empty strings.

### Readmission label distribution

| Readmission label | Encounters | Percentage |
|---|---:|---:|
| NO | 54,864 | 53.91% |
| >30 | 35,545 | 34.93% |
| <30 | 11,357 | 11.16% |

The `readmitted` column has three categories:

- `NO`: no recorded readmission.
- `<30`: readmitted within 30 days.
- `>30`: readmitted after 30 days.

---

## 8. Readmission Analysis

For the descriptive SQL analysis, the 30-day readmission rate was calculated as:

```sql
SUM(readmitted = '<30') * 100.0 / COUNT(*)
```

The overall recorded readmission rate was calculated as:

```sql
SUM(readmitted IN ('<30', '>30')) * 100.0 / COUNT(*)
```

The first metric measures the percentage of encounters recorded as readmitted within 30 days. The second combines both readmission categories.

These calculations use encounter records as the denominator, not unique patients.

### 8.1 Readmission by admission type

| Admission type | Total encounters | Within 30 days | After 30 days | Not readmitted | 30-day rate | Overall recorded rate |
|---|---:|---:|---:|---:|---:|---:|
| Emergency | 53,990 | 6,221 | 19,309 | 28,460 | 11.52% | 47.29% |
| Urgent | 18,480 | 2,066 | 6,452 | 9,962 | 11.18% | 46.09% |
| NULL | 5,291 | 586 | 2,231 | 2,474 | 11.08% | 53.24% |
| Elective | 18,869 | 1,961 | 5,746 | 11,162 | 10.39% | 40.84% |
| Not Available | 4,785 | 495 | 1,721 | 2,569 | 10.34% | 46.31% |
| Newborn | 10 | 1 | 2 | 7 | 10.00% | 30.00% |
| Not Mapped | 320 | 27 | 84 | 209 | 8.44% | 34.69% |
| Trauma Center | 21 | 0 | 0 | 21 | 0.00% | 0.00% |

**Interpretation**

- Emergency admissions had the highest 30-day readmission rate among the main recognised admission categories at 11.52%.
- Urgent admissions followed at 11.18%.
- The difference between emergency and urgent admissions was 0.34 percentage points.
- Elective admissions had a 10.39% rate.
- The category mapped to the literal description `NULL` had a 53.24% overall recorded readmission rate.

Newborn and Trauma Center have very small encounter counts. Their percentages should not be treated as reliable comparisons.

The admission-type mapping value `NULL` is a text description in the mapping table, not proof that the original ID is SQL NULL.

### 8.2 Readmission by admission source

| Admission source | Encounters | Within 30 days | After 30 days | Not readmitted | 30-day rate | Overall recorded rate |
|---|---:|---:|---:|---:|---:|---:|
| Transfer from hospital inpatient / same facility, separate claim | 12 | 2 | 3 | 7 | 16.67% | 41.67% |
| HMO Referral | 187 | 29 | 58 | 100 | 15.51% | 46.52% |
| Not Mapped | 161 | 22 | 81 | 58 | 13.66% | 63.98% |
| Court/Law Enforcement | 16 | 2 | 4 | 10 | 12.50% | 37.50% |
| Transfer from Skilled Nursing Facility | 855 | 101 | 236 | 518 | 11.81% | 39.42% |
| Emergency Room | 57,494 | 6,720 | 21,667 | 29,107 | 11.69% | 49.37% |
| Physician Referral | 29,565 | 3,130 | 9,640 | 16,795 | 10.59% | 43.19% |
| NULL | 6,781 | 706 | 2,458 | 3,617 | 10.41% | 46.66% |
| Not Available | 125 | 13 | 16 | 96 | 10.40% | 23.20% |
| Clinic Referral | 1,104 | 111 | 310 | 683 | 10.05% | 38.13% |
| Transfer from a hospital | 3,187 | 309 | 672 | 2,206 | 9.70% | 30.78% |
| Transfer from another health care facility | 2,264 | 212 | 398 | 1,654 | 9.36% | 26.94% |
| Extramural Birth | 2 | 0 | 0 | 2 | 0.00% | 0.00% |
| Transfer from critical access hospital | 8 | 0 | 2 | 6 | 0.00% | 25.00% |
| Normal Delivery | 2 | 0 | 0 | 2 | 0.00% | 0.00% |
| Transfer from Ambulatory Surgery Center | 2 | 0 | 0 | 2 | 0.00% | 0.00% |
| Sick Baby | 1 | 0 | 0 | 1 | 0.00% | 0.00% |

**Interpretation**

- The highest percentage was 16.67% for transfer from a hospital inpatient/same facility separate claim, based on only 12 encounters.
- HMO Referral had a 15.51% rate based on 187 encounters.
- Emergency Room was the largest admission-source category, with 57,494 encounters and an 11.69% rate.
- Physician Referral accounted for 29,565 encounters, with a 10.59% rate.

The categories with small numbers of encounters should be interpreted cautiously. The largest categories provide more stable descriptive comparisons, although they do not establish causation.

### 8.3 Readmission by discharge destination

| Discharge destination | Encounters | Within 30 days | After 30 days | Not readmitted | 30-day rate | Overall recorded rate |
|---|---:|---:|---:|---:|---:|---:|
| Still patient / expected to return for outpatient services | 3 | 2 | 0 | 1 | 66.67% | 66.67% |
| Medicare approved swing bed | 63 | 28 | 18 | 17 | 44.44% | 73.02% |
| Admitted as inpatient to this hospital | 21 | 9 | 2 | 10 | 42.86% | 52.38% |
| Psychiatric hospital | 139 | 51 | 34 | 54 | 36.69% | 61.15% |
| Rehabilitation facility | 1,993 | 552 | 519 | 922 | 27.70% | 53.74% |
| Another inpatient care institution | 1,184 | 247 | 350 | 587 | 20.86% | 50.42% |
| Another short-term hospital | 2,128 | 342 | 668 | 1,118 | 16.07% | 47.46% |
| Skilled Nursing Facility | 13,954 | 2,046 | 4,916 | 6,992 | 14.66% | 49.89% |
| Medicaid nursing facility | 48 | 7 | 16 | 25 | 14.58% | 47.92% |
| Left AMA | 623 | 90 | 221 | 312 | 14.45% | 49.92% |
| Home IV provider | 108 | 15 | 38 | 55 | 13.89% | 49.07% |
| ICF | 815 | 104 | 278 | 433 | 12.76% | 46.87% |
| Home with home health service | 12,902 | 1,638 | 5,362 | 5,902 | 12.70% | 54.26% |
| NULL | 3,691 | 459 | 1,027 | 2,205 | 12.44% | 40.26% |
| Discharged to home | 60,234 | 5,602 | 21,517 | 33,115 | 9.30% | 45.02% |
| Not Mapped | 989 | 92 | 376 | 521 | 9.30% | 47.32% |
| Long-term care hospital | 412 | 30 | 144 | 238 | 7.28% | 42.23% |
| Hospice / medical facility | 372 | 24 | 7 | 341 | 6.45% | 8.33% |
| Hospice / home | 399 | 19 | 36 | 344 | 4.76% | 13.78% |
| Neonate discharged to another hospital | 6 | 0 | 4 | 2 | 0.00% | 66.67% |
| Expired | 1,642 | 0 | 0 | 1,642 | 0.00% | 0.00% |
| Referred to another institution for outpatient services | 11 | 0 | 6 | 5 | 0.00% | 54.55% |
| Referred to this institution for outpatient services | 14 | 0 | 5 | 9 | 0.00% | 35.71% |
| Expired at home | 8 | 0 | 0 | 8 | 0.00% | 0.00% |
| Expired in a medical facility | 2 | 0 | 0 | 2 | 0.00% | 0.00% |
| Federal healthcare facility | 5 | 0 | 1 | 4 | 0.00% | 20.00% |

**Interpretation**

- The highest reported percentage was 66.67% for the category still patient/expected to return for outpatient services, based on three encounters.
- Medicare approved swing beds had a 44.44% rate based on 63 encounters.
- Rehabilitation facilities had a 27.70% rate based on 1,993 encounters.
- Skilled Nursing Facility discharges accounted for 13,954 encounters and had a 14.66% rate.
- Discharge to home was the largest category, with 60,234 encounters and a 9.30% rate.

These categories are not interchangeable. Expired and hospice categories are particularly different from ordinary discharges and should not be interpreted as evidence of lower clinical risk.

---

## 9. Diagnosis Analysis

The diagnosis columns are:

- `diag_1`: Primary diagnosis.
- `diag_2`: Secondary diagnosis.
- `diag_3`: Additional secondary diagnosis.

The codes are represented as ICD-9 codes in the source dataset.

### 9.1 Most frequent primary diagnosis codes

| Diagnosis code | Encounters |
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
| 780 | 2,019 |
| 996 | 1,967 |
| 276 | 1,889 |
| 38 | 1,688 |
| 250.8 | 1,680 |
| 599 | 1,595 |
| 584 | 1,520 |
| V57 | 1,207 |
| 250.6 | 1,183 |
| 518 | 1,115 |

Code 428 was the most frequent primary diagnosis code, with 6,862 encounters.

### 9.2 Diagnosis occurrences by position

The SQL query combined all three diagnosis columns using `UNION ALL` and counted occurrences by diagnosis position and code.

Some of the highest occurrence counts were:

| Diagnosis position | Code | Occurrences |
|---|---|---:|
| Additional secondary | 250 | 11,555 |
| Additional secondary | 401 | 8,289 |
| Primary | 428 | 6,862 |
| Secondary | 276 | 6,752 |
| Secondary | 428 | 6,662 |
| Primary | 414 | 6,581 |
| Secondary | 250 | 6,071 |
| Additional secondary | 276 | 5,175 |
| Secondary | 427 | 5,036 |
| Additional secondary | 428 | 4,577 |

`UNION ALL` was used so that repeated diagnosis codes were retained as separate occurrences rather than removed as duplicates.

### 9.3 Primary diagnosis and 30-day readmission

The query considered primary diagnosis codes with at least 100 encounters.

| Primary diagnosis | Encounters | Within 30 days | 30-day readmission rate |
|---|---:|---:|---:|
| V58 | 228 | 95 | 41.67% |
| 443 | 110 | 24 | 21.82% |
| 593 | 101 | 21 | 20.79% |
| 572 | 239 | 49 | 20.50% |
| 202 | 104 | 20 | 19.23% |
| 250.7 | 871 | 165 | 18.94% |
| 790 | 144 | 27 | 18.75% |
| 250.6 | 1,183 | 219 | 18.51% |
| 787 | 267 | 49 | 18.35% |
| 707 | 257 | 43 | 16.73% |
| 294 | 116 | 19 | 16.38% |
| 571 | 277 | 45 | 16.25% |
| 434 | 2,028 | 329 | 16.22% |
| 537 | 111 | 18 | 16.22% |
| 808 | 136 | 22 | 16.18% |
| 444 | 156 | 25 | 16.03% |
| 440 | 840 | 133 | 15.83% |
| 820 | 1,082 | 171 | 15.80% |
| 403 | 513 | 79 | 15.40% |
| 250.82 | 412 | 63 | 15.29% |

**Interpretation**

- V58 had the highest reported 30-day readmission rate, 41.67%, among codes with at least 100 encounters.
- The V58 result was based on 228 encounters.
- Code 434 had 2,028 encounters and a 16.22% rate.
- Code 250.6 had 1,183 encounters and an 18.51% rate.

These are descriptive associations. The diagnosis codes have not yet been translated into clinical descriptions, and the results do not demonstrate that a diagnosis caused a readmission.

---

## 10. Important Analytical Decisions and Limitations

### Encounter-level versus patient-level analysis

The SQL readmission queries use encounters as their unit of analysis. A patient can contribute more than one encounter.

The percentages should therefore be described as encounter-level rates, not the percentage of unique patients readmitted.

### Missing values

The raw dataset uses `?` as a missing-value marker in several fields. SQL `IS NULL` alone will not detect these values.

The Python cleaning phase must standardise these markers before calculating missing-value percentages or applying imputation.

### Weight

Weight has 98,569 missing markers. It is excluded from the current analysis focus.

### Diagnosis descriptions

Diagnosis codes are currently analysed as codes. A separate ICD-9 reference would be needed to add reliable clinical descriptions.

### Small sample sizes

High percentages in categories with only a few records may be unstable. The denominator should always be considered alongside the percentage.

### Historical data

The dataset covers 1999–2008. Findings describe this historical dataset and should not be presented as current hospital performance.

### No causal conclusions

The SQL analysis is descriptive. It does not establish that admission type, admission source, discharge destination or diagnosis caused readmission.

---

## 11. Technical Issues to Address

### MySQL local data loading

During the rerun of SQL files 03 and 06, `LOAD DATA LOCAL INFILE` returned error 3948.

Before future imports, check:

```sql
SHOW VARIABLES LIKE 'local_infile';
```

The client and server both need local data loading enabled for `LOAD DATA LOCAL INFILE` to work.

The existing tables should not be dropped or reloaded until their current contents have been verified.

### SQL execution order

The SQL scripts should be run in dependency order when setting up a fresh database.

However, setup and import scripts should not be rerun blindly against an existing database. Check for `DROP TABLE`, `CREATE TABLE`, `TRUNCATE` and data-loading statements first.

During the latest rerun, the supplied output showed scripts 02–10. Script 01 was not included in the output provided.

---

## 12. Next Phase: Python Data Quality and Cleaning

The next development stage is to return to:

```text
notebooks/01_raw_data_inspection.ipynb
```

The notebook already contains the initial data inspection work. Continue from the existing notebook rather than repeating it.

### Step 1 — Recheck missing values

- Convert `?` to `NaN`.
- Count missing values per column.
- Calculate missing-value percentages.
- Review columns with high missingness.
- Keep weight outside the current analysis focus.

### Step 2 — Check duplicates and identifiers

- Check duplicate rows.
- Confirm encounter ID uniqueness.
- Inspect repeated patient numbers.
- Preserve the difference between encounter records and unique patients.

### Step 3 — Review data types

Potential numeric columns include:

- `encounter_id`
- `patient_nbr`
- `time_in_hospital`
- `num_lab_procedures`
- `num_procedures`
- `num_medications`
- `number_outpatient`
- `number_emergency`
- `number_inpatient`
- `number_diagnoses`

These should be checked and converted carefully. Diagnosis codes should remain categorical rather than being treated as ordinary continuous measurements.

### Step 4 — Handle categorical variables

Review:

- Gender
- Age group
- Race
- Admission type
- Admission source
- Discharge destination
- Diagnosis codes
- Medication indicators
- Readmission label

Use the mapping tables to make ID fields understandable.

### Step 5 — Create a cleaned dataset

Save the cleaned data separately, for example:

```text
data/processed/diabetic_data_cleaned.csv
```

Do not overwrite the raw CSV.

### Step 6 — Exploratory data analysis

Create visualisations for:

- Age distribution.
- Gender distribution.
- Encounter frequency.
- Readmission categories.
- Readmission by admission type.
- Readmission by admission source.
- Readmission by discharge destination.
- Frequent diagnosis codes.
- Medication patterns.

### Step 7 — Predictive modelling

After cleaning and exploratory analysis, investigate whether the available encounter information can support a readmission prediction task.

Potential workflow:

1. Define the target variable.
2. Examine class imbalance.
3. Separate training and test data appropriately.
4. Prevent patient-level data leakage by considering repeated encounters for the same patient.
5. Build a baseline model.
6. Evaluate precision, recall, F1-score, ROC-AUC and PR-AUC.
7. Interpret model results and limitations.

A patient-aware split is important because the same patient can have multiple encounters. Randomly splitting encounter rows could place records from the same patient in both training and test sets.

The timing and availability of each feature must also be reviewed to avoid using information that would not have been known at the prediction point.

---

## 13. Project Completion Checklist

### Completed

- [x] Initial Python raw-data inspection.
- [x] Dataset structure and column inspection.
- [x] Missing-marker investigation.
- [x] MySQL database and raw table setup.
- [x] Raw encounter data available in MySQL.
- [x] Initial SQL data inspection.
- [x] Patient encounter frequency analysis.
- [x] Duplicate encounter ID check.
- [x] SQL data-quality checks.
- [x] Admission-type mapping analysis.
- [x] Admission-source mapping analysis.
- [x] Discharge-destination mapping analysis.
- [x] Diagnosis frequency analysis.
- [x] Diagnosis-position analysis.
- [x] Primary diagnosis and 30-day readmission analysis.

### Remaining

- [ ] Resolve and verify MySQL local import configuration for future imports.
- [ ] Finish and validate the final README and project notes.
- [ ] Continue Python data-quality analysis.
- [ ] Standardise missing values.
- [ ] Complete Python data cleaning.
- [ ] Create exploratory visualisations.
- [ ] Prepare a final analytical report.
- [ ] Investigate and build a suitable predictive model.
- [ ] Evaluate and document model limitations.
- [ ] Update GitHub with the completed project documentation and analysis.

---

## 14. Overall Project Status

The SQL phase has completed the initial encounter inspection, patient-level encounter frequency checks, data-quality checks, mapping-table analysis, readmission comparisons and diagnosis analysis.

The SQL results provide a foundation for the next phase.

The next priority is to continue Python data cleaning and exploratory analysis using the existing notebook, while preserving the original raw dataset.

**Important:** All readmission results in this report are descriptive encounter-level statistics from the supplied SQL output. They should not be interpreted as causal or clinical conclusions.
