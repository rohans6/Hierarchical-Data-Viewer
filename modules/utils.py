import os

def get_dir_path(): 
    full_path=os.path.dirname(os.path.abspath(__file__))
    return "\\".join(full_path.split("\\")[:-1])

def getFullPath(filename):
    crtdir = os.path.dirname(__file__)
    pardir = os.path.abspath(os.path.join(crtdir, os.pardir))
    return f"{pardir}/{filename}"

