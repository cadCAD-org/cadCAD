from runtime import run
from ui import config1, config2
from tabulate import tabulate
result = run.main()
print(tabulate(result, headers='keys', tablefmt='psql'))