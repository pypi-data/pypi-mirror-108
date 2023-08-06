import argparse

from packagecake import bake, generate_report


def _print_cake(namespace: argparse.Namespace) -> None:
    cake, cake_name = bake(namespace.package)
    print(f"{cake} - {cake_name}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="python -m packagecake",
        description="Bake a packagecake or discover PyPI packagecake stats",
    )
    parser.set_defaults(func=lambda x: x)
    subparsers = parser.add_subparsers(help="sub-command help")

    bake_parser = subparsers.add_parser("bake", help="bake help")
    bake_parser.add_argument(
        "package", action="store", help="Name of the package to bake. Ex: requests"
    )
    bake_parser.set_defaults(func=_print_cake)

    stats_parser = subparsers.add_parser("stats", help="stats help")
    stats_parser.set_defaults(func=generate_report)
    args = parser.parse_args()
    args.func(args)
