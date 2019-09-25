from pyspark.sql import SparkSession
from pyspark.context import SparkContext
import os

os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3'
os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/local/bin/python3'

spark = SparkSession\
        .builder\
        .appName("distroduce")\
        .getOrCreate()

spark_context: SparkContext = spark.sparkContext
print(f"Spark UI: {spark_context.uiWebUrl}")
print()