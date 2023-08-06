from pathlib import Path
import os

def ensure_file_path(filepath):
    """
    Functions makes sure all folders in a given file path exist. Creates them if they don't.
    """
    try:
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
    except Exception as e:
        raise e from None

def docker_find_mount_point(iterations=10):
    """Find mountpoint of jupyter docker so we dont have to use relative imports"""
    if os.path.ismount('.'):
        return '.'
    else: 
        path='..'
        i=0
        while not os.path.ismount(path) and i<iterations:
            i+=1
            path+='/..'
        if i != iterations:
            return path
        else:
            print(f"Couldnt find root within {iterations} iterations")