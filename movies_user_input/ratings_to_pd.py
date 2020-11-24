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

# Read ratings from HDFS
ratingsDf = spark.read.parquet("hdfs:///user/root/data/MOV/PARQUET/ratings.parquet").drop("timestamp")


# Splitting training data
serveDf = ratingsDf.limit(1000).randomSplit([0.01,0.99], seed=12345)

# Store data to serve as pandas split json
serveDf[0].toPandas().to_json('/code/mlf_data.json', orient='split')
