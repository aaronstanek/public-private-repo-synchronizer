import os
import shutil
import pathlib
import json

CONFIG_FILE_NAME = ".synchronizer-config.json"

def read_config(SYNC_SOURCE):

    config_file_path = os.path.join(SYNC_SOURCE, CONFIG_FILE_NAME)
    
    if not os.path.exists(config_file_path):
        return []

    try:
        with open(config_file_path, "r") as file:
            config = json.loads(file.read())
    except:
        print(f"Could not interpret source ${CONFIG_FILE_NAME} as valid json")
        print("Stopping Sync")
        exit(1)
    
    if type(config) != dict:
        print(f"Expected the top-level entity in source ${CONFIG_FILE_NAME} to be an object")
        print("Stopping Sync")
        exit(1)
    
    if "ignore" not in config:
        return []

    ignore = config["ignore"]

    if type(ignore) != list:
        print(f"Expected ignore entity in source ${CONFIG_FILE_NAME} to be an array")
        print("Stopping Sync")
        exit(1)
    
    for element in ignore:
        if type(element) != str or len(element) == 0:
            print(f"Expected elements of ignore entity in source ${CONFIG_FILE_NAME} to be non-empty strings")
            print("Stopping Sync")
            exit(1)
    
    return ignore

def ignore_from_source(SYNC_SOURCE):

    ignore = [CONFIG_FILE_NAME] + read_config(SYNC_SOURCE)

    for element in ignore:
        full_path = os.path.join(SYNC_SOURCE, element)
        if not os.path.exists(full_path):
            continue
        if os.path.isdir(full_path):
            shutil.rmtree(full_path)
        else:
            pathlib.Path(full_path).unlink()
