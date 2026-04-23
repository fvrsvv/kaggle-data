{{ config(
    materialized='table',
    catalog='clickhouse',
    schema='gold',
    engine='MergeTree()',
    order_by='industry, education_level'
) }}

SELECT 
    industry,
    education_level,
    COUNT(*) AS job_count,
    AVG(salary) AS avg_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    approx_percentile(salary, 0.5) AS median_salary,
    COUNT(DISTINCT job_title) AS unique_job_titles,
    AVG(experience_years) AS avg_experience,
    MAX(ingestion_date) AS last_updated
    -- now() AS dbt_loaded_at
FROM {{ source('silver', 'job_salary_prediction') }}
GROUP BY industry, education_level
ORDER BY avg_salary DESC