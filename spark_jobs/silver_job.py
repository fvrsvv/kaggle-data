from pyspark.sql import SparkSession
from pyspark.sql.functions import col, lower, trim, current_date, current_timestamp, lit

spark = SparkSession.builder \
    .appName("Raw_to_Silver_Job") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.read.json("s3a://raw/job_salary_prediction_dataset.json")

df_clean = (df
    .dropDuplicates(["job_title", "industry", "education_level", "salary"])
    .filter((col("salary").isNotNull()) & (col("salary") > 0))
    .withColumn("job_title", lower(trim(col("job_title"))))
    .withColumn("industry", lower(trim(col("industry"))))
    .withColumn("education_level", lower(trim(col("education_level"))))
    .withColumn("ingestion_date", current_date())
    .withColumn("load_timestamp", current_timestamp())
    .withColumn("source", lit("kaggle"))
)

spark.sql("CREATE NAMESPACE IF NOT EXISTS iceberg.silver")

df_clean.writeTo("iceberg.silver.job_salary_prediction") \
    .tableProperty("format-version", "2") \
    .option("write.format.default", "parquet") \
    .createOrReplace()

print("✅ Successfully written to Iceberg table with Nessie: iceberg.silver.job_salary_prediction")
spark.stop()