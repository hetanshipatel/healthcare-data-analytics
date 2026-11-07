
-- Healthcare Analytics Project
-- Step 2: Create the raw data table

USE healthcare_analytics;

CREATE TABLE IF NOT EXISTS raw_diabetic_data (

    encounter_id VARCHAR(255),
    patient_nbr VARCHAR(255),
    race VARCHAR(255),
    gender VARCHAR(255),
    age VARCHAR(255),
    weight VARCHAR(255),

    admission_type_id VARCHAR(255),
    discharge_disposition_id VARCHAR(255),
    admission_source_id VARCHAR(255),

    time_in_hospital VARCHAR(255),
    payer_code VARCHAR(255),
    medical_specialty VARCHAR(255),

    num_lab_procedures VARCHAR(255),
    num_procedures VARCHAR(255),
    num_medications VARCHAR(255),

    number_outpatient VARCHAR(255),
    number_emergency VARCHAR(255),
    number_inpatient VARCHAR(255),

    diag_1 VARCHAR(255),
    diag_2 VARCHAR(255),
    diag_3 VARCHAR(255),

    number_diagnoses VARCHAR(255),
    max_glu_serum VARCHAR(255),
    A1Cresult VARCHAR(255),

    metformin VARCHAR(255),
    repaglinide VARCHAR(255),
    nateglinide VARCHAR(255),
    chlorpropamide VARCHAR(255),
    glimepiride VARCHAR(255),
    acetohexamide VARCHAR(255),
    glipizide VARCHAR(255),
    glyburide VARCHAR(255),
    tolbutamide VARCHAR(255),
    pioglitazone VARCHAR(255),
    rosiglitazone VARCHAR(255),
    acarbose VARCHAR(255),
    miglitol VARCHAR(255),
    troglitazone VARCHAR(255),
    tolazamide VARCHAR(255),
    examide VARCHAR(255),
    citoglipton VARCHAR(255),
    insulin VARCHAR(255),
    glyburide_metformin VARCHAR(255),
    glipizide_metformin VARCHAR(255),
    glimepiride_pioglitazone VARCHAR(255),
    metformin_rosiglitazone VARCHAR(255),
    metformin_pioglitazone VARCHAR(255),

    `change` VARCHAR(255),
    diabetesMed VARCHAR(255),
    readmitted VARCHAR(255)

) ENGINE=InnoDB DEFAULT CHARACTER SET utf8mb4;

-- Check that the table was created
SHOW TABLES;

-- Inspect the table structure
DESCRIBE raw_diabetic_data;
