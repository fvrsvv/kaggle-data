from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, lit
from minio import Minio
from minio.error import S3Error


def download_to_silver():
    spark = SparkSession.builder \
            .appName("raw_to_silver_job_salary") \
            .config("spark.hadoop.fs.s3a.endpoint",          "http://minio:9000") \
            .config("spark.hadoop.fs.s3a.access.key",        "minio") \
            .config("spark.hadoop.fs.s3a.secret.key",        "minio123") \
            .config("spark.hadoop.fs.s3a.path.style.access", "true") \
            .config("spark.hadoop.fs.s3a.impl",              "org.apache.hadoop.fs.s3a.S3AFileSystem") \
            .config("spark.sql.extensions",                  "io.delta.sql.DeltaSparkSessionExtension") \
            .config("spark.sql.catalog.spark_catalog",       "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
            .getOrCreate()
    
    recent_file = ['s3://raw/job_salary_prediction_dataset.json']
    df = spark.read.json(*recent_file)

    df.write.parquet("data.parquet")

    client = Minio(
        endpoint="minio:9000",          
        access_key="minio",
        secret_key="minio123",
        secure=False
    )
    bucket_name = "silver"
    object_name = "data.parquet"

    try:
        client.put_object(bucket_name, object_name, content_type="application/parquet")
        print(f"Sucsessful loaded: {bucket_name}/{object_name} byte)")
    except S3Error as err:
        print(f"Error MinIO: {err}")

if __name__ == "__main__":
    download_to_silver()

    

dag = DAG(
    dag_id="raw_to_silver",
    schedule_interval=None,
    catchup=False,
)

raw_to_silver = PythonOperator(
    task_id="raw_to_silver",
    python_callable=download_to_silver(),
    dag=dag,
)

(raw_to_silver)
