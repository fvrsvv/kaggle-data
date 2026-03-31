from airflow.operators.bash import BashOperator
from airflow import DAG

dag = DAG(
    dag_id="dbt_job_salary_run",
    schedule_interval=None,
    schedule=None,
    catchup=False,
    tags=["dbt", "clickhouse"],
)

dbt_run = BashOperator(
    task_id="dbt_run",
    bash_command="""
        cd /opt/airflow/dags/dbt/job_salary && 
        dbt run --select silver+ gold+ --profiles-dir /opt/airflow/dags/dbt
    """,
    dag=dag,
)

dbt_test = BashOperator(
    task_id="dbt_test",
    bash_command="""
        cd /opt/airflow/dags/dbt/job_salary && 
        dbt deps && 
        dbt run --select silver+ gold+ &&
        dbt test --select silver+ gold+
    """,
    dag=dag,
)

(dbt_test >> dbt_run)