{{ config(
    materialized = 'table',
    file_format = 'iceberg'
) }}

SELECT 
    industry,
    COUNT(*) AS vacancy_count,
    ROUND(AVG(salary), 2) AS avg_salary,
    ROUND(MEDIAN(salary), 2) AS median_salary,
    MIN(salary) AS min_salary,
    MAX(salary) AS max_salary,
    ROUND(STDDEV(salary), 2) AS salary_stddev
FROM {{ source('silver', 'job_salary_prediction') }}
GROUP BY industry
ORDER BY avg_salary DESC