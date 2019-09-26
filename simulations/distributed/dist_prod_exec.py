from pprint import pprint

import pandas as pd
from tabulate import tabulate

from simulations.distributed.spark.session import spark_context as sc
from simulations.regression_tests import config1, config2

from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from cadCAD.utils import arrange_cols
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Distributed Execution")
dist_proc_ctx = ExecutionContext(context=exec_mode.dist_proc)
run = Executor(exec_context=dist_proc_ctx, configs=configs, spark_context=sc)
# pprint(dist_proc_ctx)

# print(configs)
i = 0
config_names = ['config1', 'config2']
for raw_result, tensor_field in run.execute():
    result = arrange_cols(pd.DataFrame(raw_result), False)
    print()
    # print(f"Tensor Field: {config_names[i]}")
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result, headers='keys', tablefmt='psql'))
    print()
    i += 1