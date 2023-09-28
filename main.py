"""
    Author: RepentStar
    Github: https://github.com/RepentStar
    Date: 2023/9/23
"""

from utils import *


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
    logger.setLevel(logging.DEBUG)
    logger.disabled = True

    try:
        change_list, invalid_files = rename(get_custom_path())
        cli_print_yellow(f"Change List:{change_list}")
        cli_print_green("Done!")
        cli_print_red(f"Unrecognized file:{invalid_files}")
    except:
        print("Error!Please open the logger to check.")


if __name__ == "__main__":
    cli_print_yellow("不删除任何文件，只改变文件名。")
    main()
