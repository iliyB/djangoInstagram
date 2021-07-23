import os

def create_folder(folder: str):
    if not os.path.isdir(folder):
        os.mkdir(folder)

def delete_file(file: str):
    if os.path.isfile(file):
        os.remove(file)