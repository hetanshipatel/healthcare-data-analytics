USE healthcare_analytics;

SELECT
    m.description AS discharge_destination,
    COUNT(*) AS total_encounters,

    SUM(r.readmitted = '<30') AS readmitted_within_30_days,
    SUM(r.readmitted = '>30') AS readmitted_after_30_days,
    SUM(r.readmitted = 'NO') AS not_readmitted,

    ROUND(
        SUM(r.readmitted = '<30') * 100.0 / COUNT(*), 2
    ) AS readmission_rate_within_30_days,

    ROUND(
        SUM(r.readmitted IN ('<30', '>30')) * 100.0 / COUNT(*), 2
    ) AS overall_recorded_readmission_rate

FROM raw_diabetic_data r

LEFT JOIN discharge_disposition_mapping m
    ON r.discharge_disposition_id = m.discharge_disposition_id

GROUP BY r.discharge_disposition_id, m.description
ORDER BY readmission_rate_within_30_days DESC;