{{ config(materialized='view', tags=['iceberg_setup']) }}

CREATE TABLE IF NOT EXISTS silver_job_salary_iceberg (
    job_title           String,
    experience_years    Nullable(Int8),
    educational_level   String,
    skills_count        Nullable(Int8),
    industry            String,
    company_size        String,
    location            String,
    remote_work         String,
    certification       Nullable(Int8),
    salary              Int32,
    ingestion_date      Date,
    load_timestamp      DateTime,
    source              String
)
ENGINE = IcebergS3(
    'http://minio:9000/silver/silver/job_salary_prediction',
    'minio',
    'minio123'
)
SETTINGS 
    allow_experimental_iceberg = 1;