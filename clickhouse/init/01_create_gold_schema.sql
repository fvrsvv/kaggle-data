CREATE DATABASE IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.fct_salary_overview (
    industry            String,
    education_level     String,
    avg_salary          Float64,
    job_count           Int64,
    min_salary          Float64,
    max_salary          Float64,
    unique_job_titles   Int64,
    last_updated        Date,
    dbt_loaded_at       DateTime
) ENGINE = MergeTree()
ORDER BY (industry, education_level);