from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="silver_to_gold_dbt",
    start_date=datetime(2025, 1, 1),
    schedule=None,
    catchup=False,
    default_args=default_args,
    tags=["dbt", "iceberg", "clickhouse"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_create_view",
        bash_command="""
            cd /opt/airflow/dags/dbt/job_salary && 
            dbt deps &&
            dbt run --target dev_trino --select gold+
        """,
    )

    # insert_to_clickhouse = SQLExecuteQueryOperator(
    #     task_id="insert_into_clickhouse",
    #     conn_id="trino",         
    #     sql="""
    #         INSERT INTO clickhouse.gold.fct_salary_overview
    #         SELECT * FROM iceberg.silver_gold.fct_salary_overview
            
    #     """,
    #     autocommit=True,
    # )
        
    insert_to_clickhouse = SQLExecuteQueryOperator(
        task_id="insert_into_clickhouse",
        conn_id="trino",         
        sql="""
            INSERT INTO clickhouse.gold.fct_salary_overview
            SELECT 
                -- String → VARBINARY для LowCardinality(String)
                CAST(industry AS VARBINARY) as industry,
                CAST(education_level AS VARBINARY) as education_level,
                avg_salary,
                job_count,
                min_salary,
                max_salary,
                unique_job_titles,
                last_updated,
                -- TIMESTAMP(6) → TIMESTAMP(0)
                CAST(dbt_loaded_at AS TIMESTAMP(0)) as dbt_loaded_at
            FROM iceberg.silver_gold.fct_salary_overview
        """,
        autocommit=True,
    )

    dbt_run >> insert_to_clickhouse