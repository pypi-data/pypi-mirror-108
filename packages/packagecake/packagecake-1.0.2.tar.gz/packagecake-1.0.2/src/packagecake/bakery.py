"""
Functions to take a package and bake it into a cake

>>> import packagecake
>>> packagecake.bake("requests")
🍰 - Shortcake
"""
import hashlib
import math
from typing import Tuple, Union

Cake = str


def bake(pkg_name: str) -> Tuple[Cake, str]:
    """
    Takes the name of a package and produces its cake.

    Args:
        pkg_name (str): Name of a package.

    Returns:
        Cake: a delicious packagecake
    """
    cakes = [
        ("🍥", "Fish Cake"),
        ("🥮", "Moon Cake"),
        ("🎂", "Birthday Cake"),
        ("🍰", "Shortcake"),
        ("🧁", "Cupcake"),
        ("", ""),
        ("", ""),
        ("🍩", "Donut"),
    ]

    signature = pkg_name
    while cakes:
        cake_item = cakes.pop()
        value = _compute_signature(signature)
        if value % 2:
            return cake_item
        signature = value
    return cake_item


def _compute_signature(value: Union[str, int]) -> int:
    """
    Produces a consistent integer representation of the provided input

    Args:
        value (Union[str, int]): an string or integer

    Returns:
        int: output integer
    """
    if isinstance(value, str):
        return int(hashlib.sha256(value.encode("utf-8")).hexdigest(), 16)

    return int(math.sqrt(value))


def pypi_stats() -> None:
    """
    Produces a report details the type and count of packagecake found
    on PyPI
    """
