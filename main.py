"""
    Author: RepentStar
    Github: https://github.com/RepentStar
    Date: 2023/9/23
"""

from utils import *
import logging
import rich
from rich.logging import RichHandler


def main() -> None:
    """
    Refactored function to improve readability and maintainability.

    Args:
        None

    Returns:
        None
    """
    logging.basicConfig(
        format="%(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[RichHandler(rich_tracebacks=True)],
    )
    logger = logging.getLogger("rich")
    logger.setLevel(logging.DEBUG)
    logger.disabled = False
    console = rich.get_console()
    print("不删除任何文件，只改变文件名。")
    try:
        change_list, invalid_files = rename(logger, get_custom_path(logger))
        console.log(
            "Change List:{change_list}".format(change_list=change_list), style="yellow"
        )
        console.log("Done!", style="green")
        console.log(
            "Unrecognized file:{invalid_files}".format(
                invalid_files=invalid_files, style="bold red"
            ),
        )
    except:
        console.log(
            "[bold red]Error![/bold red] Please open the logger to check.",
            log_locals=True,
        )


if __name__ == "__main__":
    main()
