#!/home/romana/.virtualenvs/checker_env/bin/python3

import subprocess


def create_app():
    return subprocess.run(["flask", "run", "--host=0.0.0.0"],
                          capture_output=False)


create_app()
