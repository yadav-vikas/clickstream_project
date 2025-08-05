from pyspark.sql import SparkSession
from pyspark.sql.functions import col
from pyspark.sql.types import StringType

from pyspark.sql import SparkSession
from pyspark.sql.functions import explode, split
from pyspark.sql.types import StructType, StructField, StringType


spark = SparkSession.builder \
    .appName("SnowplowKafkaToHDFS") \
    .config("spark.hadoop.fs.defaultFS", "hdfs://namenode:9000") \
    .getOrCreate()

# Read from Kafka
# df = spark.readStream \
#     .format("kafka") \
#     .option("kafka.bootstrap.servers", "kafka:9094") \
#     .option("subscribe", "collector-good") \
#     .option("startingOffsets", "earliest") \
#     .load()

# # Parse Kafka value as string
# parsed_df = df.selectExpr("CAST(value AS STRING)").withColumn("event", col("value").cast(StringType()))

# print("DF COUNT AFTER PARSING:", parsed_df.count())

# # Write to HDFS (append mode)
# query = parsed_df.writeStream \
#     .format("text") \
#     .option("path", "/output") \
#     .option("checkpointLocation", "/checkpoint") \
#     .outputMode("append") \
#     .start()

# query.awaitTermination()

#
# A PySpark Structured Streaming example demonstrating how to correctly
# set up and terminate a streaming query to avoid the "LiveListenerBus is stopped" error.
#
# This script reads from a simple socket source and writes the word count
# to the console.
#
# To run this example locally, you will need a Spark installation.
# You can submit this script using `spark-submit`.
# For the socket source, you can use `nc -lk 9999` in a separate terminal
# to send data.
#

# Main function to encapsulate the streaming logic
def main():
    # Create a SparkSession. The `getOrCreate()` method is crucial
    # as it reuses an existing session if one is available.
    # Set log level to WARN to reduce verbosity in the console output
    spark.sparkContext.setLogLevel("WARN")

    # Define a schema for the streaming data. This is often good practice
    # and required for certain sources. For a simple socket source,
    # the schema is just a single string column.
    schema = StructType([
        StructField("value", StringType(), True)
    ])

    try:
        print("Starting the streaming query...")

        # Create a streaming DataFrame from the socket source.
        # This will simulate a continuous stream of data.
        # In a real-world scenario, you would replace this with your
        # Kafka, file, or other streaming source.
        lines = spark.readStream \
            .format("socket") \
            .option("host", "kafka") \
            .option("port", 9094) \
            .load(schema=schema)

        # Split the lines into words and explode them into separate rows
        words = lines.select(explode(split(lines.value, " ")).alias("word"))

        # Generate a running word count
        wordCounts = words.groupBy("word").count()

        # Start the streaming query to write the results to the console.
        # `trigger` is an optional setting for how often to process new data.
        query = wordCounts.writeStream \
            .outputMode("complete") \
            .format("console") \
            .option("truncate", "false") \
            .trigger(processingTime="5 seconds") \
            .start()

        print("Streaming query started. To send data, use `nc -lk 9094` in a terminal.")
        print("Waiting for termination... Press Ctrl+C to stop the application.")
        print("Query count: ", query.count())
        # This is the critical line to prevent your error.
        # `awaitTermination()` blocks the current thread until the query terminates.
        # Without this, the script would end immediately after starting the query,
        # which would stop the Spark session and cause the error on subsequent operations.
        query.awaitTermination()

    except Exception as e:
        print(f"An error occurred during the streaming process: {e}")
    finally:
        # Stop the SparkSession when the application is gracefully terminated
        # or an exception occurs. This ensures resources are released.
        print("Stopping SparkSession.")
        spark.stop()

# Entry point for the script
if __name__ == "__main__":
    main()


