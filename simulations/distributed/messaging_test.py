import pandas as pd
from tabulate import tabulate

from simulations.distributed.spark.session import spark_context as sc
from simulations.distributed import messaging

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
for raw_result, tensor_field in run.execute():
    result = arrange_cols(pd.DataFrame(raw_result), False)
    print()
    print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
    print("Output:")
    print(tabulate(result.head(1), headers='keys', tablefmt='psql'))
    print(tabulate(result.tail(1), headers='keys', tablefmt='psql'))
    print()
    i += 1
