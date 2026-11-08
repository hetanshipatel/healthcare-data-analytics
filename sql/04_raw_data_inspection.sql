-- =====================================================
-- PROJECT: Healthcare Data Analytics & Data Quality Monitoring
-- FILE: 04_raw_data_inspection.sql
-- PURPOSE: Initial SQL profiling of raw diabetes data
-- =====================================================

USE healthcare_analytics;


-- 1. TOTAL NUMBER OF RECORDS
SELECT
    COUNT(*) AS total_records
FROM raw_diabetic_data;


-- 2. COUNT DISTINCT ENCOUNTERS
SELECT
    COUNT(DISTINCT encounter_id) AS distinct_encounters
FROM raw_diabetic_data;


-- 3. COUNT DISTINCT PATIENTS
SELECT
    COUNT(DISTINCT patient_nbr) AS distinct_patients
FROM raw_diabetic_data;


-- 4. CHECK FOR DUPLICATE ENCOUNTER IDs
SELECT
    encounter_id,
    COUNT(*) AS occurrences
FROM raw_diabetic_data
GROUP BY encounter_id
HAVING COUNT(*) > 1
ORDER BY occurrences DESC
LIMIT 20;


-- 5. CHECK MINIMUM AND MAXIMUM ENCOUNTER IDs
SELECT
    MIN(CAST(encounter_id AS UNSIGNED)) AS first_encounter_id,
    MAX(CAST(encounter_id AS UNSIGNED)) AS last_encounter_id
FROM raw_diabetic_data;


-- 6. PATIENTS WITH MULTIPLE ENCOUNTERS
SELECT
    patient_nbr,
    COUNT(*) AS number_of_encounters
FROM raw_diabetic_data
GROUP BY patient_nbr
HAVING COUNT(*) > 1
ORDER BY number_of_encounters DESC
LIMIT 20;


-- 7. OVERALL PATIENT ENCOUNTER STATISTICS
SELECT
    COUNT(*) AS total_unique_patients,
    SUM(number_of_encounters > 1) AS patients_with_multiple_encounters,
    MAX(number_of_encounters) AS highest_encounters_for_one_patient
FROM (
    SELECT
        patient_nbr,
        COUNT(*) AS number_of_encounters
    FROM raw_diabetic_data
    GROUP BY patient_nbr
) AS patient_counts;


-- 8. DISTRIBUTION OF ENCOUNTERS PER PATIENT
SELECT
    number_of_encounters,
    COUNT(*) AS number_of_patients
FROM (
    SELECT
        patient_nbr,
        COUNT(*) AS number_of_encounters
    FROM raw_diabetic_data
    GROUP BY patient_nbr
) AS patient_counts
GROUP BY number_of_encounters
ORDER BY number_of_encounters;


-- 9. GENDER DISTRIBUTION
SELECT
    gender,
    COUNT(*) AS total_records
FROM raw_diabetic_data
GROUP BY gender
ORDER BY total_records DESC;


-- 10. AGE GROUP DISTRIBUTION
SELECT
    age,
    COUNT(*) AS total_records
FROM raw_diabetic_data
GROUP BY age
ORDER BY age;


-- 11. ADMISSION TYPE DISTRIBUTION
SELECT
    admission_type_id,
    COUNT(*) AS total_records
FROM raw_diabetic_data
GROUP BY admission_type_id
ORDER BY total_records DESC;


-- 12. READMISSION DISTRIBUTION
SELECT
    readmitted,
    COUNT(*) AS total_records,
    ROUND(
        COUNT(*) * 100.0 /
        (SELECT COUNT(*) FROM raw_diabetic_data),
        2
    ) AS percentage
FROM raw_diabetic_data
GROUP BY readmitted
ORDER BY total_records DESC;


-- 13. MISSING VALUE MARKERS ('?')
SELECT
    SUM(race = '?') AS race_missing,
    SUM(payer_code = '?') AS payer_code_missing,
    SUM(medical_specialty = '?') AS medical_specialty_missing,
    SUM(diag_1 = '?') AS diag_1_missing,
    SUM(diag_2 = '?') AS diag_2_missing,
    SUM(diag_3 = '?') AS diag_3_missing
FROM raw_diabetic_data;


-- 14. CHECK ACTUAL NULL AND EMPTY VALUES
SELECT
    SUM(race IS NULL OR TRIM(race) = '') AS race_null_or_empty,
    SUM(payer_code IS NULL OR TRIM(payer_code) = '') AS payer_code_null_or_empty,
    SUM(medical_specialty IS NULL OR TRIM(medical_specialty) = '') AS specialty_null_or_empty,
    SUM(diag_1 IS NULL OR TRIM(diag_1) = '') AS diag_1_null_or_empty,
    SUM(diag_2 IS NULL OR TRIM(diag_2) = '') AS diag_2_null_or_empty,
    SUM(diag_3 IS NULL OR TRIM(diag_3) = '') AS diag_3_null_or_empty
FROM raw_diabetic_data;


-- =====================================================
-- END OF RAW DATA INSPECTION
-- =====================================================