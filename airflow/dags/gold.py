from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, count, avg, median, min, max, stddev, 
    round as spark_round, when
)
import logging

def get_spark_session():
    return SparkSession.builder \
    .appName("silver_to_gold_vitrines") \
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
    .getOrCreate()

# mart 1: salary by industry
def salary_by_industry():
    spark = get_spark_session()
    try:
        df_silver = spark.read.format("delta").load("s3a://silver/job_salary_prediction")
        df_mart = (df_silver.groupBy("industry")
            .agg(
                count("*").alias("vacancy_count"),
                spark_round(avg("salary"), 2).alias("avg_salary"),
                spark_round(median("salary"), 2).alias("median_salary"),
                min("salary").alias("min_salary"),
                max("salary").alias("max_salary"),
                spark_round(stddev("salary"), 2).alias("salary_stddev")
            )
            .orderBy(col("avg_salary").desc())
        )
        df_mart.write \
            .format("delta") \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .save("s3a://gold/salary_by_industry")
        logging.info(f"Витрина gold.salary_by_industry создана ({df_mart.count()} строк)")
        df_mart.show(10, truncate=False)
    finally:
        spark.stop()

# mart 2: salary by experience
def salary_by_experience():
    spark = get_spark_session()
    try:
        df_silver = spark.read.format("delta").load("s3a://silver/job_salary_prediction")
        
        df_with_category = df_silver.withColumn(
            "experience_category",
            when(col("experience_years") < 2, "Junior (0-1 год)")
            .when((col("experience_years") >= 2) & (col("experience_years") < 5), "Middle (2-4 года)")
            .when((col("experience_years") >= 5) & (col("experience_years") < 8), "Senior (5-7 лет)")
            .otherwise("Lead/Principal (8+ лет)")
        )

        df_mart = (df_with_category.groupBy("experience_category", "education_level")
            .agg(
                count("*").alias("vacancy_count"),
                spark_round(avg("salary"), 2).alias("avg_salary"),
                spark_round(median("salary"), 2).alias("median_salary"),
                spark_round(min("salary"), 2).alias("min_salary"),
                spark_round(max("salary"), 2).alias("max_salary")
            )
            .orderBy(col("experience_category"), col("education_level"))
        )
        df_mart.write \
            .format("delta") \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .save("s3a://gold/salary_by_experience_edu")
        logging.info(f"Витрина gold.salary_by_experience_edu создана ({df_mart.count()} строк)")
        df_mart.show(20, truncate=False)
    finally:
        spark.stop()

# marts: salary summary by remote work and company size
def salary_summary():
    spark = get_spark_session()
    try:
        df_silver = spark.read.format("delta").load("s3a://silver/job_salary_prediction")
        df_mart = (df_silver.groupBy("remote_work", "company_size")
            .agg(
                count("*").alias("vacancy_count"),
                spark_round(avg("salary"), 2).alias("avg_salary"),
                spark_round(median("salary"), 2).alias("median_salary")
            )
            .orderBy(col("avg_salary").desc())
        )
        df_mart.write \
            .format("delta") \
            .mode("overwrite") \
            .option("overwriteSchema", "true") \
            .save("s3a://gold/salary_summary")
        logging.info(f"Витрина gold.salary_summary создана ({df_mart.count()} строк)")
        df_mart.show(20, truncate=False)
    finally:
        spark.stop()

