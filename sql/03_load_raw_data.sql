
-- Healthcare Analytics Project
-- Step 3: Import original CSV into the raw table

USE healthcare_analytics;

LOAD DATA LOCAL INFILE
'C:/Projects/healthcare-data-analytics/data/raw/diabetic_data.csv'

INTO TABLE raw_diabetic_data

FIELDS TERMINATED BY ','
OPTIONALLY ENCLOSED BY '"'

LINES TERMINATED BY '\n'
IGNORE 1 LINES

(
    encounter_id,
    patient_nbr,
    race,
    gender,
    age,
    weight,
    admission_type_id,
    discharge_disposition_id,
    admission_source_id,
    time_in_hospital,
    payer_code,
    medical_specialty,
    num_lab_procedures,
    num_procedures,
    num_medications,
    number_outpatient,
    number_emergency,
    number_inpatient,
    diag_1,
    diag_2,
    diag_3,
    number_diagnoses,
    max_glu_serum,
    A1Cresult,
    metformin,
    repaglinide,
    nateglinide,
    chlorpropamide,
    glimepiride,
    acetohexamide,
    glipizide,
    glyburide,
    tolbutamide,
    pioglitazone,
    rosiglitazone,
    acarbose,
    miglitol,
    troglitazone,
    tolazamide,
    examide,
    citoglipton,
    insulin,
    glyburide_metformin,
    glipizide_metformin,
    glimepiride_pioglitazone,
    metformin_rosiglitazone,
    metformin_pioglitazone,
    `change`,
    diabetesMed,
    @readmitted
)

SET readmitted = TRIM(TRAILING '\r' FROM @readmitted);

-- Verify imported records
SELECT COUNT(*) AS total_records
FROM raw_diabetic_data;

-- Preview the imported data
SELECT *
FROM raw_diabetic_data
LIMIT 5;
