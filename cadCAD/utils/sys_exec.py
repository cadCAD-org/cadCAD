import warnings

from pyspark import RDD, Row
from pyspark.sql import DataFrame, SparkSession
import pandas as pd

# Distributed
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


def to_pandas_df(rdd: RDD, init_condition: dict = None):
    # Typefull
    if init_condition is not None:
        return to_spark(rdd, init_condition).toPandas()
    # Typeless
    else:
        return to_pandas(rdd)


def to_spark_df(rdd: RDD, spark: SparkSession, init_condition: dict = None):
    # Typefull
    if init_condition is not None:
        return to_spark(rdd, init_condition)
    # Typeless
    else:
        spark.conf.set("spark.sql.execution.arrow.enabled", "true")
        spark.conf.set("spark.sql.execution.arrow.fallback.enabled", "true")
        warnings.simplefilter(action='ignore', category=UserWarning)
        pdf_from_rdd: DataFrame = to_pandas(rdd)
        result = spark.createDataFrame(pdf_from_rdd)
        del pdf_from_rdd
        return result
