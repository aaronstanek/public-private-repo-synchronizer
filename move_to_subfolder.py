import os
import shutil
import json

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
    
    if "path" not in config:
        return None
    
    subfolder_path = config["path"]

    if type(subfolder_path) != str or len(subfolder_path) == 0:
        print(f"Expected path in destination ${CONFIG_FILE_NAME} to be a non-empty string")
        print("Stopping Sync")
        exit(1)
    
    return subfolder_path

def move_folder_contents(source_dir, dest_dir):

    for item in os.listdir(source_dir):

        if item == "." or item == "..":
            continue

        shutil.move(os.path.join(source_dir, item), dest_dir)

def move_to_subfolder(SYNC_SOURCE):

    subfolder_path = read_config()

    if subfolder_path is None:
        return SYNC_SOURCE
    
    copy_target = os.path.join("temp-for-subfolder-path", subfolder_path)
    
    os.makedirs(copy_target)

    move_folder_contents(SYNC_SOURCE, copy_target)

    move_folder_contents("temp-for-subfolder-path", SYNC_SOURCE)

    return os.path.join(SYNC_SOURCE, subfolder_path)
