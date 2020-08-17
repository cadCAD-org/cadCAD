import warnings
from pprint import pprint

from pyspark import RDD, Row
from pyspark.sql import DataFrame, SparkSession
import pandas as pd

# Distributed
from tabulate import tabulate


def align_type(init_condition: dict):
    def f(d):
        for y, x in init_condition.items():
            d[y] = type(x)(d[y])
        return Row(**d)
    return f

### Typefull Conversion: to Spark
# rdd -> spark
### Typeless Conversion: to Spark
# (rdd -> pandas) -> spark
def to_spark(rdd: RDD, init_condition: dict):
    type_aligner = align_type(init_condition)
    rdd: RDD = rdd.map(type_aligner)
    return rdd.toDF()

### Typefull Conversion: to Pandas
# (rdd -> spark) -> pandas
### Typeless Conversion: to Pandas
# rdd -> pandas
def to_pandas(rdd: RDD):
    rdd_result: RDD = rdd.collect()
    pdf_from_rdd: DataFrame = pd.DataFrame(rdd_result)
    del rdd_result
    return pdf_from_rdd


def to_pandas_df(rdd: RDD, string_conversion=False, init_condition: dict = None):
    if init_condition is not None and string_conversion is False:
        # Typefull
        return to_spark(rdd=rdd, init_condition=init_condition).toPandas()
    elif init_condition is None and string_conversion is True:
        # String
        return rdd.map(lambda d: Row(**dict([(k, str(v)) for k, v in d.items()]))).toDF()
    else:
        # Typeless
        return to_pandas(rdd)


def to_spark_df(rdd: RDD, spark: SparkSession = None, init_condition: dict = None):
    if init_condition is not None and spark is not None:
        # Typefull
        return to_spark(rdd, init_condition)
    elif spark is None and init_condition is None:
        # String
        return rdd.map(lambda d: Row(**dict([(k, str(v)) for k, v in d.items()]))).toDF()
    else:
        # Typeless
        spark.conf.set("spark.sql.execution.arrow.enabled", "true")
        spark.conf.set("spark.sql.execution.arrow.fallback.enabled", "true")
        warnings.simplefilter(action='ignore', category=UserWarning)
        pdf_from_rdd: DataFrame = to_pandas(rdd)
        result = spark.createDataFrame(pdf_from_rdd)
        del pdf_from_rdd
        return result
