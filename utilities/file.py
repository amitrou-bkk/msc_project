import json
import os
import numpy as np
import shutil

def get_filename_and_extension(filename):
        file_name, file_extension = os.path.splitext(filename)
        return file_name, file_extension

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def write_json(contents, dest_file):
    json_object = json.dumps(contents, indent=4)
    with open(dest_file, "w") as outfile:
        outfile.write(json_object)

def save_array_to_file(arr, filename):
   np.save(filename, arr)

def load_file_to_array(filename):
    return np.load(filename)

def write_text_to_file(text, filename):
    with open(filename, "a") as f:
        f.write(text)

def copyfile(source_file, target_file):
    shutil.copyfile(source_file, target_file)

def moveFile(source_file, target_file):
    try:
        copyfile(source_file, target_file)
        os.remove(source_file)
    except Exception as e:
        print(e)

def getDirNameFromFile(file):
    return os.path.dirname(file)

def fileOrDirectoryExists(fileOrDirectory):
    return os.path.exists(fileOrDirectory)

def createDirectory(directoryPath):
    os.makedirs(directoryPath)