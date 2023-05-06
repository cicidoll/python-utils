from pathlib import Path
import os

def exists_path(path: Path) -> None:
    """ 检测路径是否存在，不存在则创建 """
    if path.exists() == False: os.makedirs(path)

def is_exists_file(file_path: Path) -> bool:
    """ 检测文件是否存在 """
    return file_path.exists()