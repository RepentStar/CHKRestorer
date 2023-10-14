import logging
import os
from typing import List, Tuple, Optional
import filetype  # type: ignore
import sys
import rich
from rich.logging import RichHandler


class CHKRestorer:
    def __init__(self, path=None, debug=False):
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

    def _get_files(self, path):
        file_list = []
        for root, dirs, files in os.walk(path):
            self.logger.debug(f"Files_in_path: {files}")
            for file in files:
                if file.endswith(".chk") or file.endswith(".CHK"):
                    file_list.append(os.path.join(root, file))
        return file_list

    def _check_type(self, files):
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

    def _rename(self):
        invalid_files = []
        available_files = []
        path = self.path
        self.logger.debug(f"Path: {path}")
        files = self._get_files(path)
        self.logger.debug(f"Chk_files: {files}")
        os.chdir(path)  # type: ignore

        for file, type in self._check_type(files):
            if type is None:
                invalid_files.append(file)
            else:
                os.rename(file, file + "." + type)
                available_files.append(file)

        return invalid_files, available_files

    def _get_custom_path(self):
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
                "Unrecognized file:{invalid_files}".format(invalid_files=invalid_files),
                style="bold red",
            )
        except Exception as err:
            self.console.log(
                "[bold red]Error![/bold red] Please open the logger to check."
            )
            self.console.log(err)
            raise
