from datetime import datetime
from airflow import DAG
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'retries': 1,
}

with DAG(
    dag_id="raw_to_silver_spark",
    default_args=default_args,
    schedule=None,
    start_date=datetime(2025, 1, 1),
    catchup=False,
    tags=["spark", "minio", "iceberg"],
) as dag:

    bronze_to_silver = SparkSubmitOperator(
        task_id="bronze_to_silver_etl",
        application="/opt/spark_jobs/etl_raw_to_silver.py",   # путь внутри Airflow контейнера
        conn_id="spark_default",                              # берётся из AIRFLOW_CONN_...
        deploy_mode="client",
        conf={
            "spark.executor.memory": "2g",
            "spark.executor.cores": "2",
            "spark.driver.memory": "1g",
        },
        verbose=True,
        dag=dag,
    )