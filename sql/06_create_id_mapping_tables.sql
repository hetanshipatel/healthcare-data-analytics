-- =====================================================
-- FILE: 06_create_id_mapping_tables.sql
-- PURPOSE: Create lookup table for admission types
-- =====================================================

USE healthcare_analytics;

CREATE TABLE IF NOT EXISTS admission_type_mapping (
    admission_type_id VARCHAR(10) PRIMARY KEY,
    description VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS discharge_disposition_mapping (
    discharge_disposition_id INT PRIMARY KEY,
    description VARCHAR(500)
);

CREATE TABLE IF NOT EXISTS admission_source_mapping (
    admission_source_id INT PRIMARY KEY,
    description VARCHAR(500)
);

LOAD DATA LOCAL INFILE
'C:/Projects/healthcare-data-analytics/data/processed/admission_type_mapping.csv'
INTO TABLE admission_source_mapping
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE
'C:/Projects/healthcare-data-analytics/data/processed/discharge_disposition_mapping.csv'
INTO TABLE discharge_disposition_mapping
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

LOAD DATA LOCAL INFILE
'C:/Projects/healthcare-data-analytics/data/processed/admission_source_mapping.csv'
INTO TABLE admission_source_mapping
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\r\n'
IGNORE 1 LINES;

SELECT COUNT(*) AS total_discharge_mappings
FROM discharge_disposition_mapping;

SELECT COUNT(*) AS total_admission_source_mappings
FROM admission_source_mapping;

SELECT COUNT(*) AS total_admission_type_mappings
FROM admission_type_mapping;

SELECT * FROM discharge_disposition_mapping
ORDER BY discharge_disposition_id;

SELECT * FROM admission_source_mapping
ORDER BY admission_source_id;

SELECT * FROM admission_type_mapping
ORDER BY admission_type_id;