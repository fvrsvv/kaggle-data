from pyspark.sql import SparkSession

spark = SparkSession.builder \
    .appName("TestJob_From_Airflow") \
    .master("spark://spark-master:7077") \
    .getOrCreate()

df = spark.createDataFrame([(1, "hello"), (2, "world")], ["id", "text"])
df.show()

print("✅ Spark job completed successfully from Airflow!")

spark.stop()