CREATE DATABASE IF NOT EXISTS gold;

CREATE TABLE IF NOT EXISTS gold.fct_salary_overview (
    industry            LowCardinality(String),
    education_level     LowCardinality(String),
    avg_salary          Float64,
    job_count           UInt64,
    min_salary          Float64,
    max_salary          Float64,
    unique_job_titles   UInt64,
    last_updated        Date,
    dbt_loaded_at       DateTime DEFAULT now()
) ENGINE = MergeTree()
ORDER BY (industry, education_level)
SETTINGS index_granularity = 8192;