from flask import Flask
import subprocess
app = Flask(__name__)


@app.route('/')
def hello_world():
    cmd = subprocess.run(
        ["docker", "container", "ls"], capture_output=True)
    cmd_output = cmd.stdout
    cmd_stderr = cmd.stderr
    list_container = cmd_output.splitlines()
    print(list_container)
    dict_container = {}
    i = 0
    for x in list_container:
        dict_container[i] = str(x)
        i = i+1
    if cmd_output:
        return dict_container
    else:
        return cmd_stderr
