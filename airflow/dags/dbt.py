from airflow import DAG
from airflow.operators.bash import BashOperator
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
    is_paused_upon_creation=False,
    tags=["dbt", "iceberg", "clickhouse"],
) as dag:

    dbt_gold = BashOperator(
        task_id="dbt_gold_layer",
        bash_command="""
            cd /opt/airflow/dags/dbt/job_salary && 
            dbt deps &&
            dbt run --target dev_trino --select gold+ --full-refresh
        """,
    )
    
    dbt_gold