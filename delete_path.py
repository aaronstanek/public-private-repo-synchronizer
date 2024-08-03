import os
import shutil
import pathlib

def delete_path(full_path):
    while len(full_path) > 0 and full_path[-1] == "/":
        full_path = full_path[:-1]
    if not os.path.exists(full_path):
        return
    if os.path.islink(full_path) or os.path.isfile(full_path):
        pathlib.Path(full_path).unlink()
    else:
        shutil.rmtree(full_path)
