import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.validation import config_udc_json3
from cadCAD import configs


exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()
first_config = configs # only contains config1
single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run = Executor(exec_context=single_proc_ctx, configs=first_config)

raw_result, tensor_field = run.main()
result = pd.DataFrame(raw_result)
result = pd.concat([result.drop(['c'], axis=1), result['c'].apply(pd.Series)], axis=1)

# print(list(result['c']))

# print(tabulate(result['c'].apply(pd.Series), headers='keys', tablefmt='psql'))

print()
print("Tensor Field: config1")
print(tabulate(tensor_field, headers='keys', tablefmt='psql'))
print("Output:")
print(tabulate(result, headers='keys', tablefmt='psql'))
print()
print(result.info(verbose=True))

# def f(df, col):
#     for k in df[col].iloc[0].keys():
#         df[k] = None
#     for index, row in df.iterrows():
#         # df.apply(lambda row:, axis=1)