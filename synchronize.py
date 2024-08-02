import os
import shutil

from commit_and_upload import commit_and_upload

for environment_variable_name in ["GH_TOKEN", "SYNC_SOURCE", "SYNC_GH_URL"]:
    if environment_variable_name not in os.environ:
        print(f"{environment_variable_name} not available")
        print("Stopping Sync")
        exit(1)
    if len(os.environ[environment_variable_name]) == 0:
        print(f"{environment_variable_name} has length 0")
        print("Stopping Sync")
        exit(1)

SYNC_SOURCE = os.path.join("source", os.environ["SYNC_SOURCE"])
SYNC_GH_URL = os.environ["SYNC_GH_URL"]

if not os.path.isdir(SYNC_SOURCE):
    print("SYNC_SOURCE does not correspond to a directory")
    print("Stopping Sync")
    exit(1)

shutil.move("destination/.git", SYNC_SOURCE)

commit_and_upload(SYNC_SOURCE, SYNC_GH_URL)

print("Sync Complete")
