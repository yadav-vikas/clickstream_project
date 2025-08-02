from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

spark = SparkSession.builder \
    .appName("SnowplowKafkaToHDFS") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Read from Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "snowplow-enriched") \
    .option("startingOffsets", "latest") \
    .load()

# Parse Kafka value as string
parsed_df = df.selectExpr("CAST(value AS STRING)").withColumn("event", col("value").cast(StringType()))

# Write to HDFS (append mode)
query = parsed_df.writeStream \
    .format("text") \
    .option("path", "/output") \
    .option("checkpointLocation", "/checkpoint") \
    .outputMode("append") \
    .start()

query.awaitTermination()
