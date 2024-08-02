import os
import shutil
import pathlib
import json

from delete_path import delete_path

CONFIG_FILE_NAME = ".synchronizer-config.json"

def read_config():

    config_file_path = os.path.join("destination", CONFIG_FILE_NAME)

    if not os.path.exists(config_file_path):
        return []

    try:
        with open(config_file_path, "r") as file:
            config = json.loads(file.read())
    except:
        print(f"Could not interpret destination ${CONFIG_FILE_NAME} as valid json")
        print("Stopping Sync")
        exit(1)
    
    if type(config) != dict:
        print(f"Expected the top-level entity in destination ${CONFIG_FILE_NAME} to be an object")
        print("Stopping Sync")
        exit(1)
    
    if "lock" not in config:
        return []

    lock = config["lock"]

    if type(lock) != list:
        print(f"Expected lock entity in destination ${CONFIG_FILE_NAME} to be an array")
        print("Stopping Sync")
        exit(1)
    
    for element in lock:
        if type(element) != str or len(element) == 0:
            print(f"Expected elements of lock entity in destination ${CONFIG_FILE_NAME} to be non-empty strings")
            print("Stopping Sync")
            exit(1)
    
    return lock

def lock_in_destination(SYNC_SOURCE):

    lock = [".git", CONFIG_FILE_NAME] + read_config()

    for element in lock:
        source_path = os.path.join(SYNC_SOURCE, element)
        delete_path(source_path)
        relative_containing_folder_parts = list(pathlib.Path(element).parts)[:-1]
        containing_folder_path = SYNC_SOURCE
        for path_part in relative_containing_folder_parts:
            containing_folder_path = os.path.join(containing_folder_path, path_part)
            if os.path.isdir(containing_folder_path):
                continue
            delete_path(containing_folder_path)
            os.mkdir(containing_folder_path)
        shutil.move(os.path.join("destination", element), containing_folder_path)
