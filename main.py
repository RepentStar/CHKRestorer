"""
    Author: RepentStar
    Github: https://github.com/RepentStar
    Date: 2023/9/23
"""

from chkrestorer.CHKRestorer import CHKRestorer


def main():
    Restorer = CHKRestorer(debug=False)
    Restorer.execute()


if __name__ == "__main__":
    main()
