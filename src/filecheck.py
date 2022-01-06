from pathlib import Path
from datetime import datetime
import warnings
import shutil
import os


def get_mtime(file):
    return int(Path(file).stat().st_mtime)


def getcwd():
    return os.path.dirname(os.path.abspath(__file__))


def new_version(src: str, dst: str, delay: int = 30):
    """Return true if src is newer than dst, by a seconds
    interval defined by the `delay` variable"""
    src_exist = os.path.exists(src)
    dst_exist = os.path.exists(dst)

    if not src_exist:
        return False

    if not dst_exist:
        return True

    src_mtime = get_mtime(src)

    dst_mtime = get_mtime(dst)

    delta = src_mtime - dst_mtime

    if delta > delay:
        return True
    else:
        return False


def get_files(walk_path):
    src_files = {}

    for root, _, files in os.walk(walk_path, topdown=True):
        for file in files:
            file_path = os.path.join(root, file)

            src_files[file.lower()] = {"path": file_path}

    return src_files


def update_files(src_dir, dst_dir):
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    cwd = getcwd()

    src_files = get_files(src_dir)

    dst_files = get_files(dst_dir)

    for file in dst_files.keys():
        try:
            dst_file_path = dst_files[file]["path"]
            src_file_path = src_files[file]["path"]

            result = new_version(src_file_path, dst_file_path, 30)

            if result:
                shutil.copyfile(src_file_path, dst_file_path)

        except KeyError:
            with open(f"{cwd}/log.txt", "a+") as f:
                msg = f"""\n>> {now} - File '{file}' exists only at destination folder.
                Path: {dst_file_path}"""

                warnings.warn(msg)
                f.write(msg)
        except PermissionError as e:
            with open(f"{cwd}/log.txt", "a+") as f:
                msg = f"\n>> {now} - File '{file}' Unassessable.\n {e}"
                print(msg)
                f.write(msg)


def update_file(src_file, dst_file):
    cwd = getcwd()
    now = datetime.now().strftime("%d/%m/%Y %H:%M:%S")

    try:
        result = new_version(src_file, dst_file, 30)

        if result:
            shutil.copyfile(src_file, dst_file)
    except Exception as e:
        with open(f"{cwd}/log.txt", "a+") as f:
            msg = f"\n>> {now} - Source '{src_file}'; Destination '{dst_file}' \n Error: {e}"
            f.write(msg)


if __name__ == "__main__":
    # Source Folder
    src_walk_path = "/src/folder"

    # Destination Folder
    dst_walk_path = "/dst/folder"

    update_files(src_walk_path, dst_walk_path)
