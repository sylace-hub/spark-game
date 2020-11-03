# Find Spark
import findspark
findspark.init()

from pyspark.sql.types import *

from pyspark import SparkContext
from pyspark.sql import SparkSession

spark = SparkSession \
    .builder \
    .appName("Movie lens model") \
    .getOrCreate()

# Define schema for ratings dataset
ratingsStruct = [StructField("userId", IntegerType(), True),
    StructField("movieId", IntegerType(), True),
    StructField("rating", DoubleType(), True),
    StructField("timestamp", IntegerType(), True)]

ratingsSchema = StructType(ratingsStruct)

# Read ratings from HDFS
ratingsDf = spark.read.format("csv") \
    .option("header", "false") \
    .option("delimiter", "::") \
    .schema(ratingsSchema) \
    .load("file:///home/mcheghal/Documents/sylace/bcg/mllib/ml-1m/ratings.dat")


# Splitting training data
serveDf = ratingsDf.randomSplit([0.1], seed=12345)

# Store data to serve as pandas split json
serveDf[0].toPandas().head(100).to_json('~/data.json', orient='split')