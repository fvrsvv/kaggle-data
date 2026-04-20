{{ config(
    materialized='table',
    schema='gold'         
) }}

SELECT 
    industry,
    education_level,
    AVG(salary)                                      AS avg_salary,
    COUNT(*)                                         AS job_count,
    MIN(salary)                                      AS min_salary,
    MAX(salary)                                      AS max_salary,
    COUNT(DISTINCT job_title)                        AS unique_job_titles,
    MAX(ingestion_date)                              AS last_updated,
    now()                                            AS dbt_loaded_at
FROM {{ source('silver', 'job_salary_prediction') }}
GROUP BY 
    industry, 
    education_level
ORDER BY avg_salary DESC