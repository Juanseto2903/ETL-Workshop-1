-- Load the Data Warehouse (MySQL)

CREATE DATABASE IF NOT EXISTS recruitment_dw
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE recruitment_dw;

-- ---------------------------------------------------------------------
-- Dimension: Dim_Date
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS fact_application;
DROP TABLE IF EXISTS dim_date;

CREATE TABLE dim_date (
    date_key    INT PRIMARY KEY,
    full_date   DATE NOT NULL,
    year        INT NOT NULL,
    quarter     INT NOT NULL,
    month       INT NOT NULL,
    month_name  VARCHAR(20) NOT NULL,
    day_of_week VARCHAR(20) NOT NULL,
    UNIQUE KEY uq_dim_date_full_date (full_date)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Dimension: Dim_Technology
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS dim_technology;

CREATE TABLE dim_technology (
    technology_key  INT PRIMARY KEY,
    technology_name VARCHAR(100) NOT NULL,
    UNIQUE KEY uq_dim_technology_name (technology_name)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Dimension: Dim_Candidate_Profile
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS dim_candidate_profile;

CREATE TABLE dim_candidate_profile (
    profile_key INT PRIMARY KEY,
    seniority   VARCHAR(50) NOT NULL,
    yoe_range   VARCHAR(20) NOT NULL,
    UNIQUE KEY uq_dim_profile_combo (seniority, yoe_range)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Dimension: Dim_Country
-- ---------------------------------------------------------------------
DROP TABLE IF EXISTS dim_country;

CREATE TABLE dim_country (
    country_key  INT PRIMARY KEY,
    country_name VARCHAR(100) NOT NULL,
    UNIQUE KEY uq_dim_country_name (country_name)
) ENGINE=InnoDB;

-- ---------------------------------------------------------------------
-- Fact: Fact_Application
-- Grain: one row = one candidate application
-- ---------------------------------------------------------------------
CREATE TABLE fact_application (
    application_key            INT PRIMARY KEY,
    date_key                   INT NOT NULL,
    technology_key              INT NOT NULL,
    profile_key                 INT NOT NULL,
    country_key                 INT NOT NULL,
    code_challenge_score        TINYINT NOT NULL,
    technical_interview_score   TINYINT NOT NULL,
    hired_flag                  TINYINT NOT NULL,
    application_count           TINYINT NOT NULL DEFAULT 1,

    CONSTRAINT fk_fact_date
        FOREIGN KEY (date_key) REFERENCES dim_date (date_key),
    CONSTRAINT fk_fact_technology
        FOREIGN KEY (technology_key) REFERENCES dim_technology (technology_key),
    CONSTRAINT fk_fact_profile
        FOREIGN KEY (profile_key) REFERENCES dim_candidate_profile (profile_key),
    CONSTRAINT fk_fact_country
        FOREIGN KEY (country_key) REFERENCES dim_country (country_key),

    INDEX idx_fact_date (date_key),
    INDEX idx_fact_technology (technology_key),
    INDEX idx_fact_profile (profile_key),
    INDEX idx_fact_country (country_key)
) ENGINE=InnoDB;