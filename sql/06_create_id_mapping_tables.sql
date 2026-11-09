-- =====================================================
-- FILE: 06_create_id_mapping_tables.sql
-- PURPOSE: Create lookup table for admission types
-- =====================================================

USE healthcare_analytics;

CREATE TABLE IF NOT EXISTS admission_type_mapping (
    admission_type_id VARCHAR(10) PRIMARY KEY,
    description VARCHAR(100)
);

INSERT INTO admission_type_mapping
    (admission_type_id, description)
VALUES
    ('1', 'Emergency'),
    ('2', 'Urgent'),
    ('3', 'Elective'),
    ('4', 'Newborn'),
    ('5', 'Not Available'),
    ('6', 'NULL'),
    ('7', 'Trauma Center'),
    ('8', 'Not Mapped')
ON DUPLICATE KEY UPDATE
    description = VALUES(description);


-- Check the mapping table
SELECT *
FROM admission_type_mapping
ORDER BY admission_type_id;