from pyspark.sql import SparkSession
from pyspark.context import SparkContext
import os

# os.environ['PYSPARK_PYTHON'] = '/usr/local/bin/python3'
# os.environ['PYSPARK_DRIVER_PYTHON'] = '/usr/local/bin/python3'
# os.environ['OBJC_DISABLE_INITIALIZE_FORK_SAFETY'] = 'YES'

spark = SparkSession\
        .builder\
        .appName("distroduce")\
        .getOrCreate()

sc: SparkContext = spark.sparkContext
print(f"Spark UI: {sc.uiWebUrl}")
print()