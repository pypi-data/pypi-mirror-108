"""
Produces a report of the number of each cake from PyPI
"""
import re
from typing import Dict, List

import requests

from .bakery import bake

ANCHOR_PATTERN = re.compile(r"<a .+>(.+)</a>")


def generate_report(*args, **kwargs) -> None:
    names = _get_package_names()
    stats = _get_cake_stats(names)
    _print_report(stats)


def _get_package_names() -> List[str]:
    """
    Produces a list of all package names from PyPI

    Returns:
        List[str]: All package names hosted on PyPI
    """
    response = requests.get("https://pypi.org/simple/")
    response.raise_for_status()
    raw_html = response.text
    return [match[1] for match in ANCHOR_PATTERN.finditer(raw_html)]


def _get_cake_stats(names: List[str]) -> Dict[str, int]:
    """
    Produces a report with counts for each cake.

    Args:
        names (List[str]): All package names hosted on PyPI

    Returns:
        Dict[str, int]: A dictionary of cakes and their counts
    """
    stats = {}
    for cake in [bake(pkg) for pkg in names]:
        cake_display_name = f"{cake[0]} - {cake[1]}"
        if not stats.get(cake_display_name):
            stats[cake_display_name] = 1
        else:
            stats[cake_display_name] += 1

    return stats


def _print_report(stats: Dict[str, int]) -> None:
    """
    Prints a report of cake counts to stdout

    Args:
        stats (Dict[str, int]): A dictionary of cakes and their counts
    """
    sorted_stats = sorted(stats.items(), key=lambda x: x[1], reverse=True)
    print("".center(30, "-"))
    print("|" + " PyPI Package Cake Stats ".center(28) + "|")
    print("".center(30, "-"))
    for cake in sorted_stats:
        print(f"|{cake[0]}".ljust(19) + f"| {cake[1]}".ljust(9) + "|")
        print("".center(30, "-"))
