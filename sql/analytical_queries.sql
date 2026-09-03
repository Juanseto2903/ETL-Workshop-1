-- Analytical Queries and KPIs
-- One query per business requirement (R1-R5)

USE recruitment_dw;

-- ---------------------------------------------------------------------
-- R1 - Hiring Trends
-- Business Question: How do applications and hires change over time?
-- ---------------------------------------------------------------------
SELECT
    d.year,
    SUM(f.application_count) AS total_applications,
    SUM(f.hired_flag)        AS total_hired,
    ROUND(SUM(f.hired_flag) / SUM(f.application_count) * 100, 2) AS hiring_rate_pct
FROM fact_application f
JOIN dim_date d ON f.date_key = d.date_key
GROUP BY d.year
ORDER BY d.year;

-- ---------------------------------------------------------------------
-- R2 - Technology Analysis
-- Business Question: Which technologies generate the most hired
-- candidates, in number and proportion?
-- ---------------------------------------------------------------------
SELECT
    t.technology_name,
    SUM(f.application_count) AS total_applications,
    SUM(f.hired_flag)        AS total_hired,
    ROUND(SUM(f.hired_flag) / SUM(f.application_count) * 100, 2) AS hiring_rate_pct
FROM fact_application f
JOIN dim_technology t ON f.technology_key = t.technology_key
GROUP BY t.technology_name
ORDER BY total_hired DESC
LIMIT 5;

-- ---------------------------------------------------------------------
-- R3 - Candidate Profile Analysis
-- Business Question: How does the hiring rate vary by seniority level
-- and years of experience?
-- ---------------------------------------------------------------------
SELECT
    p.seniority,
    p.yoe_range,
    SUM(f.application_count) AS total_applications,
    SUM(f.hired_flag)        AS total_hired,
    ROUND(SUM(f.hired_flag) / SUM(f.application_count) * 100, 2) AS hiring_rate_pct
FROM fact_application f
JOIN dim_candidate_profile p ON f.profile_key = p.profile_key
GROUP BY p.seniority, p.yoe_range
ORDER BY hiring_rate_pct DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- R4 - Geographic Recruitment Analysis
-- Business Question: Which countries concentrate the most applications,
-- and which show better or worse hiring rates?
-- ---------------------------------------------------------------------
SELECT
    c.country_name,
    SUM(f.application_count) AS total_applications,
    SUM(f.hired_flag)        AS total_hired,
    ROUND(SUM(f.hired_flag) / SUM(f.application_count) * 100, 2) AS hiring_rate_pct
FROM fact_application f
JOIN dim_country c ON f.country_key = c.country_key
GROUP BY c.country_name
ORDER BY total_applications DESC
LIMIT 10;

-- ---------------------------------------------------------------------
-- R5 - Technical Assessment Effectiveness
-- Business Question: Which of the two technical assessments better
-- discriminates between HIRED and NOT HIRED candidates?
-- ---------------------------------------------------------------------
SELECT
    hired_flag,
    ROUND(AVG(code_challenge_score), 2)      AS avg_code_challenge_score,
    ROUND(AVG(technical_interview_score), 2) AS avg_technical_interview_score,
    SUM(application_count)                   AS total_applications
FROM fact_application
GROUP BY hired_flag
ORDER BY hired_flag;