import kagglehub
import logging
import io

from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from minio import Minio
from minio.error import S3Error
from kagglehub import KaggleDatasetAdapter

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_kaggle():
    df = kagglehub.dataset_load(KaggleDatasetAdapter.PANDAS, "nalisha/job-salary-prediction-dataset", "job_salary_prediction_dataset.csv")

    json_str = df.to_json(orient="records")

    json_bytes = json_str.encode('utf-8')
    json_stream = io.BytesIO(json_bytes)

    client = Minio(
        endpoint="minio:9000",          
        access_key="minio",
        secret_key="minio123",
        secure=False
    )
    bucket_name = "raw"
    object_name = "job_salary_prediction_dataset.json"

    try:
        client.put_object(bucket_name, object_name, json_stream, length=len(json_bytes), content_type="application/json")
        print(f"Sucsessful loaded: {bucket_name}/{object_name}  ({len(json_bytes):,} byte)")
    except S3Error as err:
        print(f"Error MinIO: {err}")

if __name__ == "__main__":
    download_kaggle()

dag = DAG(
    dag_id="to_raw",
    schedule_interval=None,
    catchup=False,
)

kaggle_to_minio_task = PythonOperator(
    task_id="to_raw",
    python_callable=download_kaggle,
    dag=dag,
)

trigger_dag_silver = TriggerDagRunOperator(
    task_id = 'trigger_dag_silver',
    trigger_dag_id='raw_to_silver_spark',
    wait_for_completion=False,
    reset_dag_run=True,
)

(kaggle_to_minio_task >> trigger_dag_silver)
