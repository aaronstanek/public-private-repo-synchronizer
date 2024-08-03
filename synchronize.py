import os

from ignore_from_source import ignore_from_source
from move_to_subfolder import move_to_subfolder
from lock_in_destination import lock_in_destination
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

ignore_from_source(SYNC_SOURCE)

move_to_subfolder(SYNC_SOURCE)

lock_in_destination(SYNC_SOURCE)

commit_and_upload(SYNC_SOURCE, SYNC_GH_URL)

print("Sync Complete")
