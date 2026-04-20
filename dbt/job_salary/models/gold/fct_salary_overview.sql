{{ config(materialized='table') }}

SELECT 
    industry,
    education_level,
    AVG(salary) AS avg_salary,
    -- MEDIAN(salary) AS median_salary,
    COUNT(*) AS job_count,
    MAX(ingestion_date) AS last_updated
FROM {{ ref('stg_job_salary') }}
GROUP BY industry, education_level