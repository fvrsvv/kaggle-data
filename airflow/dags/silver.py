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
    tags=["spark", "minio"],
) as dag:

    bronze_to_silver = SparkSubmitOperator(
        task_id="bronze_to_silver_etl",
        application="/opt/spark_jobs/etl_raw_to_silver.py",
        conn_id="spark_default",
        deploy_mode="client",
        verbose=True,
        jars=(
            "/opt/spark/jars/hadoop-aws-3.3.4.jar,"
            "/opt/spark/jars/aws-java-sdk-bundle-1.12.777.jar,"
            "/opt/spark/jars/iceberg-spark-runtime-3.5_2.12-1.5.2.jar"
        ),
        conf={
            "spark.executor.memory": "1g",
            "spark.executor.cores": "1",
            "spark.driver.memory": "1g",

            # S3 MinIO
            "spark.sql.extensions": "org.apache.iceberg.spark.extensions.IcebergSparkSessionExtensions",
            "spark.sql.catalog.iceberg": "org.apache.iceberg.spark.SparkCatalog",
            "spark.sql.catalog.iceberg.catalog-impl": "org.apache.iceberg.nessie.NessieCatalog",
            "spark.sql.catalog.iceberg.uri": "http://nessie:19120/api/v2",
            "spark.sql.catalog.iceberg.warehouse": "s3a://silver/",
            "spark.sql.catalog.iceberg.ref": "main",                    # основная ветка

            # S3 MinIO
            "spark.hadoop.fs.s3a.endpoint": "http://minio:9000",
            "spark.hadoop.fs.s3a.access.key": "minio",
            "spark.hadoop.fs.s3a.secret.key": "minio123",
            "spark.hadoop.fs.s3a.path.style.access": "true",
        },
    )