{{ config(
    materialized='table',
    catalog='clickhouse',
    schema='gold',
    engine='MergeTree()',
    order_by='(skills_count)'
) }}

SELECT 
    skills_count,
    COUNT(*)                                      AS job_count,
    AVG(salary)                                   AS avg_salary,
    MIN(salary)                                   AS min_salary,
    MAX(salary)                                   AS max_salary,
    approx_percentile(salary, 0.5)                AS median_salary,
    MAX(ingestion_date)                           AS last_updated
    -- now()                                         AS dbt_loaded_at
FROM {{ source('silver', 'job_salary_prediction') }}
GROUP BY skills_count
ORDER BY avg_salary DESC