from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

import utils as u

with DAG(
    dag_id="kaggle_job_salary_ingestion",
    start_date=datetime(2026, 3, 1),
    schedule=None,        
    catchup=False,
    tags=["kaggle", "ingestion"],
) as dag:

    download_task = PythonOperator(
        task_id="download_dataset",
        python_callable=u.download_kaggle_dataset,  
    )