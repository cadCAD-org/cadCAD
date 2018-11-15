
from SimCAD.engine import ExecutionContext, Executor
from sandboxUX import config1, config2

configs = [config1, config2]
run = Executor(ExecutionContext, configs)
result = run.main()