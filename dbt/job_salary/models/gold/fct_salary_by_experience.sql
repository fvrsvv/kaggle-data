{{ config(
    materialized='table',
    catalog='clickhouse',
    schema='gold',
    engine='MergeTree()',
    order_by='(experience_bucket)'
) }}

WITH experience_buckets AS (
    SELECT 
        CASE 
            WHEN experience_years <= 2 THEN '0-2 years'
            WHEN experience_years <= 5 THEN '3-5 years'
            WHEN experience_years <= 10 THEN '6-10 years'
            ELSE '10+ years'
        END AS experience_bucket,
        salary,
        ingestion_date
    FROM {{ source('silver', 'job_salary_prediction') }}
)

SELECT 
    experience_bucket,
    COUNT(*)                                      AS job_count,
    AVG(salary)                                   AS avg_salary,
    MIN(salary)                                   AS min_salary,
    MAX(salary)                                   AS max_salary,
    approx_percentile(salary, 0.5)                AS median_salary,
    MAX(ingestion_date)                           AS last_updated
    -- now()                                         AS dbt_loaded_at
FROM experience_buckets
GROUP BY experience_bucket
ORDER BY avg_salary DESC