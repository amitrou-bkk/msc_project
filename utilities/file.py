import json
import os
import numpy as np

def get_filename_and_extension(filename):
        file_name, file_extension = os.path.splitext(filename)
        return file_name, file_extension

def read_json(file_path):
    with open(file_path, 'r') as f:
        data = json.load(f)
    return data

def save_array_to_file(arr, filename):
   np.save(filename, arr)

def load_file_to_array(filename):
    return np.load(filename)