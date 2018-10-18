from engine import run
from tabulate import tabulate
result = run.main()
print(tabulate(result, headers='keys', tablefmt='psql'))