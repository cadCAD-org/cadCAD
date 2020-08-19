from pyspark.sql import DataFrame
from tabulate import tabulate
from cadCAD import configs
from pprint import pprint
import pandas as pd

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests.models import policy_aggregation
from cadCAD.utils.sys_exec import to_spark_df, to_pandas_df
from cadCAD.configuration.utils import configs_as_dataframe #, configs_as_objs, configs_as_dicts

from distroduce.engine.execution import transform, distributed_simulations
from distroduce.session import sc_alt as sc
from distroduce.session import spark_alt as spark

exec_mode = ExecutionMode()
distributed_sims = distributed_simulations(transform)

distributed_ctx = ExecutionContext(context=exec_mode.distributed, method=distributed_sims)
run = Executor(exec_context=distributed_ctx, configs=configs, spark_context=sc)

raw_result, tensor_fields, sessions = run.execute()
print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
pprint(sessions)

print("Configuration Data:")
configs_df = configs_as_dataframe(configs)
print(tabulate(configs_df, headers='keys', tablefmt='psql'))
print("Tensor Field:")
print(tabulate(tensor_fields[0], headers='keys', tablefmt='psql'))
print("Output:")

# RDD:
print()
print("RDD:")
result: list = raw_result.take(5)
pprint(result[:2])
# to get all results execute the following
# result: list = raw_result.collect()
print()

print("Spark DataFrame:")
sdf: DataFrame = to_spark_df(raw_result, spark, policy_aggregation.genesis_states)
# sdf: DataFrame = to_spark_df(raw_result, spark)
sdf.show(5)
print()

# Pandas :
print()
print("Pandas DataFrame:")
pdf: pd.DataFrame = to_pandas_df(raw_result, policy_aggregation.genesis_states)
# pdf: pd.DataFrame = to_pandas_df(raw_result)
print(tabulate(pdf.head(), headers='keys', tablefmt='psql'))

