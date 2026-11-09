-- =====================================================
-- FILE: 07_readmission_by_admission_type.sql
-- PURPOSE: Analyse readmission by admission type
-- =====================================================

USE healthcare_analytics;


-- 1. READMISSION COUNTS AND RATES BY ADMISSION TYPE

SELECT
    m.description AS admission_type,

    COUNT(*) AS total_encounters,

    SUM(r.readmitted = '<30')
        AS readmitted_within_30_days,

    SUM(r.readmitted = '>30')
        AS readmitted_after_30_days,

    SUM(r.readmitted = 'NO')
        AS not_readmitted,

    ROUND(
        SUM(r.readmitted = '<30') * 100.0 / COUNT(*),
        2
    ) AS readmission_rate_within_30_days,

    ROUND(
        SUM(r.readmitted IN ('<30', '>30')) * 100.0 / COUNT(*),
        2
    ) AS overall_recorded_readmission_rate

FROM raw_diabetic_data r

LEFT JOIN admission_type_mapping m
    ON r.admission_type_id = m.admission_type_id

GROUP BY
    r.admission_type_id,
    m.description

ORDER BY
    readmission_rate_within_30_days DESC;