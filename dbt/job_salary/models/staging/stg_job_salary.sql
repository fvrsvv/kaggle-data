{{ config(materialized='table') }}

SELECT 
    job_title,
    industry,
    education_level,
    salary,
    ingestion_date,
    load_timestamp,
    source
FROM {{ source('silver', 'job_salary_prediction') }}