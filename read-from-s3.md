# S3 :

Install boto3 module (if not already installed on EMR) :

```console
sudo pip3 install boto3 (Already installed on EMR)
```

### From Jupyter :

```pyhton
# Create an RDD from a file in S3
s3aDf = spark.read.csv("s3a://transtat/data/BOTS_2019_01.csv")
s3aDf.show(10)
```

### Spark-submit (Python) :

```console
sudo spark-submit s3-read.py
```

```pyhton
from pyspark.sql import SparkSession

# Initialize the session
spark = SparkSession.builder.appName("using_s3").getOrCreate()

# Create an RDD from a file in S3
s3aDf = spark.read.csv("s3a://transtat/data/BOTS_2019_01.csv")
s3aDf.show(10)
```

### Scala on Spark-shell:

```console
sudo spark-shell --packages org.apache.hadoop:hadoop-aws:2.7.7
```

```scala
val df = spark.read.csv("s3a://transtat/data/BOTS_2019_01.csv")
df.show()
```
