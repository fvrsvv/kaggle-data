from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, lit, lower, trim
from minio import Minio
from minio.error import S3Error
import logging

def download_to_silver():
    spark = SparkSession.builder \
        .appName("raw_to_silver_job_salary") \
        .master("local[*]") \
        .config("spark.jars.packages", 
                "io.delta:delta-spark_2.12:3.3.0,"
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                "com.amazonaws:aws-java-sdk-bundle:1.12.262") \
        .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minio") \
        .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
        .getOrCreate()
    
    try:
        df = spark.read.option("multiline", "true").json("s3a://raw/job_salary_prediction_dataset.json")
        logging.info(f"Прочитано строк из raw: {df.count()}")

        df_clean = (df.
                    dropDuplicates()
                    .filter(col("salary").isNotNull() & (col("salary") > 0))
                    .withColumn("job_title", lower(trim(col("job_title"))))
                    .withColumn("industry", lower(trim(col("industry"))))
                    .withColumn("education_level", lower(trim(col("education_level"))))
                    .withColumn("ingestion_date", current_date())
                    .withColumn("load_timestamp", lit(datetime.now()))
                    .withColumn("source", lit("kaggle"))
                    )
        silver_path = "s3a://silver/job_salary_prediction"
        df_clean.write.format("delta").mode("overwrite").option("overwriteSchema", "true").partitionBy("ingestion_date").save(silver_path)

        logging.info(f"Успешно записано в Delta Lake: {df_clean.count()} строк")
        df_clean.printSchema()
    except Exception as e:
        logging.error(f"Error with transform {e}")
        raise
    finally:
        spark.stop()

dag = DAG(
    dag_id="raw_to_silver_delta",
    schedule_interval=None,
    schedule=None,
    catchup=False,
    tags=["delta", "to silver"],
)

raw_to_silver_task = PythonOperator(
    task_id="raw_to_silver_delta",
    python_callable=download_to_silver,
    dag=dag,
)

(raw_to_silver_task)
