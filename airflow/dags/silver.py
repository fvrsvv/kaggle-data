from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, current_date, lit, lower, trim
from minio import Minio
from minio.error import S3Error
import logging

def raw_to_silver_job():
    spark = SparkSession.builder \
        .appName("raw_to_silver_job_salary_iceberg") \
        .master("local[*]") \
        .config("spark.jars.packages", 
                "org.apache.iceberg:iceberg-spark-runtime-3.5_2.12:1.6.1,"      
                "org.apache.hadoop:hadoop-aws:3.3.4,"
                "com.amazonaws:aws-java-sdk-bundle:1.12.262,"
                "software.amazon.awssdk:bundle:2.32.29,"                     
                "software.amazon.awssdk:url-connection-client:2.32.29") \
        .config("spark.sql.extensions", "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions") \
        .config("spark.sql.catalog.spark_catalog", "org.apache.iceberg.spark.SparkCatalog") \
        .config("spark.sql.catalog.spark_catalog.type", "hadoop") \
        .config("spark.sql.catalog.spark_catalog.warehouse", "s3a://silver/") \
        .config("spark.hadoop.fs.s3a.endpoint", "http://minio:9000") \
        .config("spark.hadoop.fs.s3a.access.key", "minio") \
        .config("spark.hadoop.fs.s3a.secret.key", "minio123") \
        .config("spark.hadoop.fs.s3a.path.style.access", "true") \
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
        .config("spark.hadoop.fs.s3a.connection.ssl.enabled", "false") \
        .config("spark.hadoop.fs.s3a.endpoint.region", "us-east-1") \
        .getOrCreate()

    try:
        df = spark.read.option("multiline", "true").json("s3a://raw/job_salary_prediction_dataset.json")
        logging.info(f"Прочитано строк из raw: {df.count()}")

        df_clean = (df
            .dropDuplicates()
            .filter(col("salary").isNotNull() & (col("salary") > 0))
            .withColumn("job_title", lower(trim(col("job_title"))))
            .withColumn("industry", lower(trim(col("industry"))))
            .withColumn("education_level", lower(trim(col("education_level"))))
            .withColumn("ingestion_date", current_date())
            .withColumn("load_timestamp", lit(datetime.now()))
            .withColumn("source", lit("kaggle"))
        )

        silver_table = "spark_catalog.silver.job_salary_prediction"

        df_clean.writeTo(silver_table) \
            .tableProperty("format-version", "2") \
            .tableProperty("write.parquet.compression-codec", "zstd") \
            .partitionedBy("ingestion_date") \
            .createOrReplace()   

        logging.info(f"Успешно записано в Iceberg таблицу {silver_table}: {df_clean.count()} строк")
        df_clean.printSchema()

        spark.sql(f"SELECT * FROM {silver_table} LIMIT 5").show()

    except Exception as e:
        logging.error(f"Ошибка при трансформации в Silver (Iceberg): {e}")
        raise
    finally:
        spark.stop()

dag = DAG(
    dag_id="raw_to_silver_iceberg",
    schedule_interval=None,
    schedule=None,
    catchup=False,
    tags=["delta", "to silver"],
)

raw_to_silver_task = PythonOperator(
    task_id="raw_to_silver_iceberg",
    python_callable=raw_to_silver_job,
    dag=dag,
)

(raw_to_silver_task)
