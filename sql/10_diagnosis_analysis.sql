-- =====================================================
-- FILE: 10_diagnosis_analysis.sql
-- =====================================================

USE healthcare_analytics;


-- A. Most common primary diagnoses

SELECT
    diag_1 AS primary_diagnosis,
    COUNT(*) AS total_encounters
FROM raw_diabetic_data
WHERE diag_1 IS NOT NULL
  AND TRIM(diag_1) <> ''
  AND diag_1 <> '?'
GROUP BY diag_1
ORDER BY total_encounters DESC
LIMIT 20;

-- B. Most common diagnoses across all three positions

SELECT
    diagnosis_position,
    diagnosis_code,
    COUNT(*) AS total_occurrences
FROM (
    SELECT 'Primary' AS diagnosis_position, diag_1 AS diagnosis_code
    FROM raw_diabetic_data

    UNION ALL

    SELECT 'Secondary', diag_2
    FROM raw_diabetic_data

    UNION ALL

    SELECT 'Additional secondary', diag_3
    FROM raw_diabetic_data
) AS all_diagnoses

WHERE diagnosis_code IS NOT NULL
  AND TRIM(diagnosis_code) <> ''
  AND diagnosis_code <> '?'

GROUP BY diagnosis_position, diagnosis_code
ORDER BY total_occurrences DESC
LIMIT 50;

-- C. Which primary diagnoses have higher 30-day readmission rates?

SELECT
    diag_1 AS primary_diagnosis,
    COUNT(*) AS total_encounters,

    SUM(readmitted = '<30') AS readmitted_within_30_days,

    ROUND(
        SUM(readmitted = '<30') * 100.0 / COUNT(*), 2
    ) AS readmission_rate_within_30_days

FROM raw_diabetic_data

WHERE diag_1 IS NOT NULL
  AND TRIM(diag_1) <> ''
  AND diag_1 <> '?'

GROUP BY diag_1

HAVING COUNT(*) >= 100

ORDER BY readmission_rate_within_30_days DESC
LIMIT 20;