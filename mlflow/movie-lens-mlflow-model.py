import sys

# Find Spark
import findspark
findspark.init()

from pyspark import SparkContext
from pyspark.sql import SparkSession
from pyspark.sql.types import *

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# Import mlflow
import mlflow
import mlflow.spark

# Define schema for movies dataset
moviesStruct = [StructField("movieId", IntegerType(), True),
    StructField("title", StringType(), True),
    StructField("genres", StringType(), True)]

moviesSchema = StructType(moviesStruct)

# Define schema for ratings dataset
ratingsStruct = [StructField("userId", IntegerType(), True),
StructField("movieId", IntegerType(), True),
StructField("rating", DoubleType(), True),
StructField("timestamp", IntegerType(), True)]

ratingsSchema = StructType(ratingsStruct)

if __name__ == "__main__":

    spark = SparkSession \
        .builder \
        .appName("Movie lens model") \
        .getOrCreate()

    # Get hyper parameters from command line
    maxIter = float(sys.argv[1]) if len(sys.argv) > 1 else 5
    regParam = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01

    print("MaxIter {}, RegParam {}.".format(maxIter, regParam))

    # Read movies from HDFS
    moviesDf = spark.read.format("csv") \
        .option("header", "false") \
        .option("delimiter", "::") \
        .schema(moviesSchema) \
        .load("file:///home/mcheghal/Documents/sylace/bcg/mllib/ml-1m/movies.dat")

    # moviesDf.show(10, False)

    # Read ratings from HDFS
    ratingsDf = spark.read.format("csv") \
        .option("header", "false") \
        .option("delimiter", "::") \
        .schema(ratingsSchema) \
        .load("file:///home/mcheghal/Documents/sylace/bcg/mllib/ml-1m/ratings.dat")

    # ratingsDf.show(10)

    # Splitting training data
    training, test = ratingsDf.randomSplit([0.8, 0.2], seed=12345)

    # Got 1000209 ratings from 6040 users on 3883 movies.
    print("Training {}, test {}.".format(training.count(), test.count()))

    als = ALS(maxIter=maxIter,
              regParam=regParam, \
              implicitPrefs=False, \
              userCol="userId", \
              itemCol="movieId", \
              ratingCol="rating", \
              coldStartStrategy="drop")

    model = als.fit(training)

    predictions = model.transform(test)
    evaluator = RegressionEvaluator(metricName="rmse", labelCol="rating", predictionCol="prediction")

    rmse = evaluator.evaluate(predictions)
    print("Root-mean-square error = " + str(rmse))

    # Log hyper parameters
    mlflow.log_param("maxIter", maxIter)
    mlflow.log_param("regParam", regParam)

    # Log some metrics
    mlflow.log_metric("rmse", rmse)

    # Lo the model
    mlflow.spark.log_model(model, "model")
    print("Model saved in run %s" % mlflow.active_run().info.run_uuid)

    spark.stop()