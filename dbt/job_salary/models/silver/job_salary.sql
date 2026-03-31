{{ config(materialized = 'view') }}

SELECT 
    job_title,
    company_name,
    location,
    salary,
    salary_currency,
    salary_min,
    salary_max,
    job_type,
    experience_level,
    education_level,
    industry,
    skills,
    remote,
    ingestion_date,
    load_timestamp,
    source
FROM silver_job_salary_iceberg