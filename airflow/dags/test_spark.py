# from datetime import datetime
# from airflow import DAG
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

# with DAG(
#     dag_id="test_spark_submit",
#     start_date=datetime(2025, 1, 1),
#     schedule=None,
#     catchup=False,
#     tags=["test", "spark"],
#     default_args={
#         "owner": "airflow",
#         "retries": 1,
#     },
# ) as dag:

#     test_job = SparkSubmitOperator(
#         task_id="test_spark_job",
#         application="/opt/spark_jobs/test_job.py",
#         conn_id="spark_default",       
#         deploy_mode="client",
#         verbose=True,
#         conf={
#             "spark.executor.memory": "1g",
#             "spark.executor.cores": "1",
#             "spark.driver.memory": "1g",
#         },
#     )

#     # test_job