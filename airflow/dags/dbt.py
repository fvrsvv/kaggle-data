from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta

default_args = {
    'owner': 'airflow',
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id="silver_to_gold_dbt",
    start_date=days_ago(1),
    schedule=None,      
    catchup=False,
    default_args=default_args,
    tags=["spark", "dbt", "gold"],
) as dag:

    dbt_run = BashOperator(
        task_id="dbt_run_gold",
        bash_command="""
                cd /opt/airflow/dags/dbt/job_salary && 
                dbt deps && dbt run
                """
        # env={
        #     "CLICKHOUSE_USER": "default",
        #     "CLICKHOUSE_PASSWORD": "clickhouse_password",
        # },
    )

    dbt_run