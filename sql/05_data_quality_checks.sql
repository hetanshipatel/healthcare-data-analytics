-- =====================================================
-- PROJECT: Healthcare Data Analytics
-- FILE: 05_data_quality_checks.sql
-- PURPOSE: Systematic data quality validation
-- =====================================================

USE healthcare_analytics;


-- 1. CHECK TOTAL RECORDS
SELECT COUNT(*) AS total_records
FROM raw_diabetic_data;


-- 2. CHECK DUPLICATE ENCOUNTER IDS
SELECT
    COUNT(*) - COUNT(DISTINCT encounter_id)
    AS duplicate_encounter_count
FROM raw_diabetic_data;


-- 3. CHECK ACTUAL NULL VALUES AND QUESTION MARK MARKERS
SELECT
        SUM(weight = '?' OR weight IS NULL) AS missing_weight,
        SUM(age = '?' OR age IS NULL) AS missing_age,
        SUM(gender = '?' OR gender IS NULL) AS missing_gender,
        SUM(readmitted = '?' OR readmitted IS NULL) AS missing_readmitted,
        SUM(race = '?' OR race IS NULL) AS missing_race,
        SUM(payer_code = '?' OR payer_code IS NULL) AS missing_payer_code,
        SUM(medical_specialty = '?' OR medical_specialty IS NULL) AS missing_specialty,
        SUM(diag_1 = '?' OR diag_1 IS NULL) AS missing_diag_1,
        SUM(diag_2 = '?' OR diag_2 IS NULL) AS missing_diag_2,
        SUM(diag_3 = '?' OR diag_3 IS NULL) AS missing_diag_3
FROM raw_diabetic_data;




-- 4. CHECK GENDER VALUES
SELECT
    gender,
    COUNT(*) AS record_count
FROM raw_diabetic_data
GROUP BY gender
ORDER BY record_count DESC;


-- 5. CHECK READMISSION VALUES
SELECT
    readmitted,
    COUNT(*) AS record_count
FROM raw_diabetic_data
GROUP BY readmitted
ORDER BY record_count DESC;


-- 6. CHECK ADMISSION TYPE VALUES
SELECT
    admission_type_id,
    COUNT(*) AS record_count
FROM raw_diabetic_data
GROUP BY admission_type_id
ORDER BY admission_type_id;


-- 7. CHECK INVALID AGE CATEGORIES
SELECT
    age,
    COUNT(*) AS record_count
FROM raw_diabetic_data
WHERE age NOT IN (
    '[0-10)', '[10-20)', '[20-30)', '[30-40)',
    '[40-50)', '[50-60)', '[60-70)', '[70-80)',
    '[80-90)', '[90-100)'
)
GROUP BY age;


-- 8. CHECK ENCOUNTERS WITH MISSING IDENTIFIERS
SELECT COUNT(*) AS records_with_missing_identifiers
FROM raw_diabetic_data
WHERE encounter_id IS NULL
   OR encounter_id = ''
   OR encounter_id = '?'
   OR patient_nbr IS NULL
   OR patient_nbr = ''
   OR patient_nbr = '?';


-- =====================================================
-- END OF DATA QUALITY CHECKS
-- =====================================================