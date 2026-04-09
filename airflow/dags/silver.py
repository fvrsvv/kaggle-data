from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

with DAG(
    dag_id="raw_to_silver_spark",
    default_args={
        "owner": "airflow",
        "retries": 1,
    },
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["spark", "minio", "iceberg"],
) as dag:

    bronze_to_silver = SparkSubmitOperator(
        task_id="bronze_to_silver_etl",
        application="/opt/spark_jobs/etl_raw_to_silver.py",   
        conn_id="spark_default",          
        deploy_mode="client",
        verbose=True,
        jars="/opt/spark/jars/hadoop-aws-3.3.4.jar,/opt/spark/jars/aws-java-sdk-bundle-1.12.777.jar",
        conf={
            "spark.executor.memory": "1g",
            "spark.executor.cores": "1",
            "spark.driver.memory": "1g",
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": "minio",
            "spark.hadoop.fs.s3a.secret.key": "minio123",
            "spark.hadoop.fs.s3a.path.style.access": "true",
            "spark.hadoop.fs.s3a.impl": "org.apache.hadoop.fs.s3a.S3AFileSystem",
            "spark.hadoop.fs.s3a.connection.ssl.enabled": "false",
            "spark.hadoop.fs.s3a.aws.credentials.provider": "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider",
        },
    )