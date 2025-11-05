import os

def get_dir_path(): 
    full_path=os.getcwd()
    return "\\".join(full_path.split("\\")[:-1])


