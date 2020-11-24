from __future__ import print_function

import sys
import animation #pip install animation
import calendar
import time 
import pandas as pd
from pyspark.sql import SparkSession
from pyspark.sql.functions import *

from py4j.java_gateway import JavaGateway


@animation.wait('bar')
def loadDFs():
    global moviesDF
    moviesDF = spark.read.parquet("hdfs:///user/root/data/MOV/PARQUET/movies.parquet")
    global ratingsDF 
    ratingsDF = spark.read.parquet("hdfs:///user/root/data/MOV/PARQUET/ratings.parquet")
    global genresDF
    genresDF = spark.read.csv("/user/root/data/MOV/CSV/genres.csv").toDF("Genre")
    genresDF.collect()

def prompt():
    print('select a genre from the list')
    genresDF.show()
    print('input value')
    global genreScan
    genreScan = scan()
    print('Press enter to confirm & load a list for this genre')

@animation.wait('bar')
def getMoviesByGenre(genre):
    print('Most Rated Movies for genre : '+ genre)

    genreDF = moviesDF.filter(moviesDF.genres.contains(genre))
    moviesByRating_counts = genreDF \
        .join(ratingsDF, "movieId") \
        .groupBy("movieId").count().alias("count").orderBy(desc("count"))
        #.groupBy("movieId").count().alias("ratings count").orderBy(desc("count"))

    moviesByRating_Full = genreDF.join(moviesByRating_counts, "movieId").dropDuplicates().orderBy(desc("count"))
    
    #select(col("count").alias("count"))
    #moviesByRating_Full.show(20, False)

    global moviesByRatingPDF
    moviesByRatingPDF = moviesByRating_Full.limit(20).toPandas()
    print('')
    print(moviesByRatingPDF)

def getMaxUserId():
    return ratingsDF.agg({"userId": "max"}).collect()[0][0]

def setNewUserId():
    global newUserId
    newUserId = getMaxUserId() + 1

def inputUserRating():
    
    setNewUserRatingDF()
    setNewUserId()

    for idx, row in moviesByRatingPDF.iterrows():
        print(row['title'])
        print('your rating : ')
        rating = scan()
        addNewUserRating(row['movieId'],rating)

def setNewUserRatingDF():
    global newUserDF
    global newUserPDF
    newUserDF = spark.createDataFrame(spark.sparkContext.emptyRDD(), ratingsDF.schema)    
    newUserPDF = newUserDF.toPandas()

def addNewUserRating(movieId,rating):
    #this is not very pretty but we can afford q&d as we are in interactive mode
    newRow = {'userId': newUserId, 'movieId': movieId, 'rating':rating, 'timestamp':calendar.timegm(time.gmtime())}
    global newUserPDF
    newUserPDF = newUserPDF.append(newRow, ignore_index=True)
    print(newUserPDF)

def scan():
    scanner = spark.sparkContext._gateway.jvm.java.util.Scanner  
    sys_in = getattr(spark.sparkContext._gateway.jvm.java.lang.System, 'in')  
    return scanner(sys_in).nextLine()

def init():
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

@animation.wait('bar')
def sparkinit():
     global spark
     spark = SparkSession\
        .builder\
        .appName("Pyspark Interactive")\
        .getOrCreate()

    # this does not work as spark context is already loaded at this point
    # log4j props need to be passed over in spark-submit specifiying a log4j.properties file
    # @see sumbmit_nologs.sh in the current directory 
    # spark.sparkContext.setLogLevel('FATAL')

if __name__ == "__main__":
   
    init()
    
    print('Loading Spark...')
    sparkinit()
    print('Done !')

    print('Loading Data...')
    loadDFs()
    print('Done !')

    prompt()
    scan()
    getMoviesByGenre(genreScan)
    inputUserRating()
    spark.stop()
