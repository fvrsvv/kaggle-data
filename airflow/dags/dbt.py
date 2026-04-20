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

    insert_to_clickhouse = SQLExecuteQueryOperator(
        task_id="insert_into_clickhouse",
        conn_id="trino",         
        sql="""
            INSERT INTO clickhouse.default.fct_salary_overview
            SELECT * FROM iceberg.silver.fct_salary_overview
        """,
        autocommit=True,
    )

    dbt_run >> insert_to_clickhouse