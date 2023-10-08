import logging
import os
from typing import List, Tuple, Optional
import filetype  # type: ignore
import sys
import rich
from rich.logging import RichHandler


class CHKRestorer:
    def __init__(self, path=None, debug: bool = False) -> None:
        logging.basicConfig(
            format="%(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
            handlers=[RichHandler(rich_tracebacks=True)],
        )
        self.logger = logging.getLogger("rich")
        self.logger.setLevel(logging.DEBUG)
        self.logger.disabled = not debug
        self.console = rich.get_console()
        self.path = path

    def _get_files(self, path: str) -> List[str]:
        """
        Get all CHK files under the specified path.

        Args:
            path (str): The path to search for CHK files.

        Returns:
            List[str]: A list of file paths for the CHK files found.
        """
        file_list = []
        for root, dirs, files in os.walk(path):
            self.logger.debug(f"Files_in_path: {files}")
            for file in files:
                if file.endswith(".chk") or file.endswith(".CHK"):
                    file_list.append(os.path.join(root, file))
        return file_list

    def _check_type(self, files: List[str]) -> List[Tuple[str, Optional[str]]]:
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

    def _rename(self) -> Tuple[List[str], List[str]]:
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
        path = self.path
        self.logger.debug(f"Path: {path}")
        files = self._get_files(path)
        self.logger.debug(f"Chk_files: {files}")
        os.chdir(path)

        for file, type in self._check_type(files):
            if type is None:
                invalid_files.append(file)
            else:
                os.rename(file, file + "." + type)
                available_files.append(file)

        return invalid_files, available_files

    def _get_custom_path(self) -> str:
        """Returns a custom path based on command line arguments.

        Args:
            None

        Returns:
            str: The custom path or "./" if no valid directory path is found.
        """
        self.logger.debug(sys.argv)

        if len(sys.argv) == 1 and self.path is None:
            self.path = "./"
        elif self.path is not None:
            self.path = os.path.normpath(self.path)
            return

        for path in sys.argv:
            if os.path.isdir(path) and os.path.exists(path):
                self.path = path
                break
        else:
            self.path = "./"

    def execute(self) -> None:
        """Executes the restorer."""
        try:
            self._get_custom_path()
            invalid_files, change_list = self._rename()
            self.console.log(
                "Change List:{change_list}".format(change_list=change_list),
                style="yellow",
            )
            self.console.log("Done!", style="green")
            self.console.log(
                "Unrecognized file:{invalid_files}".format(
                    invalid_files=invalid_files, style="bold red"
                ),
            )
        except Exception as err:
            self.console.log(
                "[bold red]Error![/bold red] Please open the logger to check."
            )
            self.console.log(err)
            raise
