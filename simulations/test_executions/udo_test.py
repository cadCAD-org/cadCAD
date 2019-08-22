import pandas as pd
from tabulate import tabulate
# The following imports NEED to be in the exact order
from cadCAD.engine import ExecutionMode, ExecutionContext, Executor
from simulations.regression_tests import udo
from cadCAD import configs

exec_mode = ExecutionMode()

print("Simulation Execution: Single Configuration")
print()



single_proc_ctx = ExecutionContext(context=exec_mode.single_proc)
run = Executor(exec_context=single_proc_ctx, configs=configs)
# cols = configs[0].initial_state.keys()
cols = [
    'increment',
    'state_udo_tracker', 'state_udo', 'state_udo_perception_tracker',
    'udo_policies', 'udo_policy_tracker',
    'timestamp'
]
raw_result, tensor_field = run.execute()
result = pd.DataFrame(raw_result)[['run', 'substep', 'timestep'] + cols]
# result = pd.concat([result.drop(['c'], axis=1), result['c'].apply(pd.Series)], axis=1)

# print(list(result['c']))

# print(tabulate(result['c'].apply(pd.Series), headers='keys', tablefmt='psql'))

# print(result.iloc[8,:]['state_udo'].ds)

# ctypes.cast(id(v['state_udo']['mem_id']), ctypes.py_object).value

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