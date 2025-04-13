from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, TimestampType, DoubleType, IntegerType
from pyspark.sql.functions import col, from_json
import logging

def main():
    # spark = SparkSession.builder.appName("SmartCityStreaming")\
    #     .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.13:3.3.2,com.datastax.spark:spark-cassandra-connector_2.12:3.0.0")\
    #     .getOrCreate()
    spark = SparkSession.builder.appName("SmartCityStreaming")\
        .config("spark.jars.packages", 
            "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,"
            "com.datastax.spark:spark-cassandra-connector_2.12:3.3.0,"
            "com.github.jnr:jnr-posix:3.1.15")\
        .config("spark.sql.streaming.kafka.bootstrap.servers", "kafka:9092")\
        .config("spark.cassandra.connection.host", "cassandra")\
        .config("spark.sql.extensions", "com.datastax.spark.connector.CassandraSparkExtensions")\
        .getOrCreate()
    spark.sparkContext.setLogLevel('INFO')

    vehicleSchema = StructType([
        StructField("id", StringType(), True),
        StructField("deviceId", StringType(), True),
        StructField("timestamp", TimestampType(), True),
        StructField("location", StringType(), True),
        StructField("speed", DoubleType(), True),
        StructField("direction", StringType(), True),
        StructField("make", StringType(), True),
        StructField("model", StringType(), True),
        StructField("year", IntegerType(), True),
        StructField("fuelType", StringType(), True),
    ])

    def read_kafka_topic(topic, schema):
        logging.info(f"Reading from Kafka topic: {topic}")
        return (spark.readStream
                .format('kafka')
                .option('kafka.bootstrap.servers', 'kafka:9092')
                .option('subscribe', topic)
                .option('startingOffsets', 'earliest')
                .load()
                .selectExpr('CAST(value AS STRING)')
                .select(from_json(col('value'), schema).alias('data'))
                .select('data.*')
                .withWatermark('timestamp', '2 minutes')
                )

    def write_to_cassandra(df, table_name, keyspace_name):
        logging.info(f"Writing to Cassandra table: {keyspace_name}.{table_name}")
        return (df.writeStream
                .foreachBatch(lambda batchDF, batchId: 
                    batchDF.write
                        .format("org.apache.spark.sql.cassandra")
                        .option("spark.cassandra.output.consistency.level", "LOCAL_ONE")
                        .option("keyspace", keyspace_name)
                        .option("table", table_name)
                        .option("confirm.truncate", "true")  # Optional, to truncate table before writing
                        .mode("append")
                        .save())
                .outputMode("append")
                .start()
                )

    vehicleDF = read_kafka_topic('vehicle_data', vehicleSchema)
    query1 = write_to_cassandra(vehicleDF, "vehicle_data", "smartcity")

    try:
        query1.awaitTermination()
    except Exception as e:
        logging.error(f"Error occurred: {e}")

if __name__ == "__main__":
    main()
