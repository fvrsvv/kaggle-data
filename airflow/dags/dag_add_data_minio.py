from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago

from airflow.sdk import ObjectStoragePath

base = ObjectStoragePath("s3://aws_default@my-bucket/")

dag = DAG(
    dag_id="dag_add_data_minio.py",
    start_date=days_ago(5),
    schedule_interval=None,
    catchup=False,
)

add_data = PythonOperator(
    task_id="add_data",
    python_callable=add(),
    dag=dag,
)

(add_data)