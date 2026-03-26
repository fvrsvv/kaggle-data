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
        .master("local[*]") \
        .config("spark.jars.packages", 
                "io.delta:delta-spark_2.12:3.2.0,"
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                "com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minio") \
        .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    df = spark.read.json("s3a://raw/job_salary_prediction_dataset.json")

    df.write.format("parquet").mode("overwrite").save("s3a://silver/job_salary_prediction")

    print("Successfully written to silver!")
    spark.stop()

dag = DAG(
    dag_id="raw_to_silver",
    schedule_interval=None,
    catchup=False,
)

raw_to_silver = PythonOperator(
    task_id="raw_to_silver",
    python_callable=download_to_silver,
    dag=dag,
)

(raw_to_silver)
