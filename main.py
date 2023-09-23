"""
    Author: RepentStar
    Github: https://github.com/RepentStar
    Date: 2023/9/23
"""

import os
from typing import List, Tuple, Optional
import filetype
import sys
import logging


def get_files(path: str) -> List[str]:
    """
    Get all CHK files under the specified path.

    Args:
        path (str): The path to search for CHK files.

    Returns:
        List[str]: A list of file paths for the CHK files found.
    """
    file_list = []
    for root, dirs, files in os.walk(path):
        logging.debug(f"Files_in_path: {files}")
        for file in files:
            if file.endswith(".chk") or file.endswith(".CHK"):
                file_list.append(os.path.join(root, file))
    return file_list


def check_type(files: List[str]) -> List[Tuple[str, Optional[str]]]:
    """
    Check the type of each file in the given list.

    Args:
        files: A list of file paths.

    Returns:
        A list of tuples containing the file path and its corresponding extension.
        If the extension cannot be determined, the extension will be None.
    """
    result = []
    for file in files:
        kind = filetype.guess(file)
        if kind is None:
            result.append((file, None))
            continue
        else:
            result.append((file, kind.extension))
    return result


def rename(path: str = "./") -> Tuple[List[str], List[str]]:
    """
    Renames files in the given path by appending their type to the filename.

    Args:
        path (str): The path where the files are located. Defaults to current directory.

    Returns:
        Tuple[List[str], List[str]]: A tuple containing two lists. The first list contains
        the names of invalid files that could not be renamed. The second list contains the
        names of the successfully renamed files.
    """
    invalid_files = []
    available_files = []
    logging.debug(f"Path: {path}")
    files = get_files(path)
    logging.debug(f"Chk_files: {files}")

    for file, type in check_type(files):
        if type is None:
            invalid_files.append(file)
        else:
            os.rename(file, file + "." + type)
            available_files.append(file)

    return invalid_files, available_files


def main() -> None:
    """
    Refactored function to improve readability and maintainability.

    Args:
        None

    Returns:
        None
    """
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        stream=sys.stdout,
    )
    logger = logging.getLogger()
    # logger.setLevel(logging.DEBUG)

    try:
        change_list, invalid_files = rename()
        print(f"\033[34mChange List:{change_list}\033[0m")
        print("\033[32mDone!\033[0m")
        print(f"\033[31mUnrecognized file:{invalid_files}\033[0m")
    except:
        print("Error!Please open the logger to check.")


if __name__ == "__main__":
    print("\033[33m不删除任何文件，只改变文件名。")
    main()
