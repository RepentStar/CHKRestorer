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
        file_name = os.path.basename(file)
        if kind is None:
            result.append((file_name, None))
            continue
        else:
            result.append((file_name, kind.extension))
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


def get_custom_path() -> str:
    """Returns a custom path based on command line arguments.

    Args:
        None

    Returns:
        str: The custom path or "./" if no valid directory path is found.
    """
    logging.debug(sys.argv)

    if len(sys.argv) == 1:
        return "./"

    for path in sys.argv:
        if os.path.isdir(path):
            return path

    return "./"


def cli_print_red(text):
    print("\033[31m" + text + "\033[0m")

def cli_print_green(text):
    print("\033[32m" + text + "\033[0m")
    
def cli_print_yellow(text):
    print("\033[33m" + text + "\033[0m")