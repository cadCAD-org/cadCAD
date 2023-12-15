import os, subprocess, json
from testing.utils import assertEqual

def test_jupyter_nbconvert_row_count():
    command = f'jupyter nbconvert --to=notebook --ExecutePreprocessor.enabled=True {os.getcwd()}/testing/tests/import_cadCAD.ipynb'
    process = subprocess.Popen(command.split(), stdout=subprocess.PIPE)
    process.communicate()
    json_path = f'{os.getcwd()}/testing/tests/cadCAD_memory_address.json'
    memory_address = json.load(open(json_path))['memory_address']
    assertEqual(type(memory_address) == str, True, "cadCAD is not importable by jupyter server")
