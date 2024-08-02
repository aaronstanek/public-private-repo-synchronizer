import os
import shutil
import pathlib

def delete_path(full_path):
    if not os.path.exists(full_path):
        return
    if os.path.isdir(full_path):
        shutil.rmtree(full_path)
    else:
        pathlib.Path(full_path).unlink()
