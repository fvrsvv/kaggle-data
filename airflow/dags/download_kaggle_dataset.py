from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
from airflow.utils.dates import days_ago

import utils as u

dag = DAG(
    dag_id="dag_parsing_kaggle",
    start_date=days_ago(5),
    schedule_interval=None,
)

download_kaggle_dataset = PythonOperator(
    task_id="download_kaggle_dataset",
    python_callable=u.download_kaggle,
    dag=dag,
)

(download_kaggle_dataset)