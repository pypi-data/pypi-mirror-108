#!/usr/bin/env python3
"""Interact with the Censys Big Query through the command line."""
import argparse

from .bigquery import CensysBigQuery


def get_parser() -> argparse.ArgumentParser:
    """Gets ArgumentParser for CLI.

    Returns:
        argparse.ArgumentParser
    """
    parser = argparse.ArgumentParser(
        description="Query Censys Big Query by providing a query string"
    )

    # Add support for custom queries
    parser.add_argument("query", type=str)
    parser.add_argument(
        "-f",
        "--format",
        type=str,
        default="screen",
        nargs="+",
        metavar="json|csv|screen",
        choices=["screen", "json", "csv"],
        help="format of output",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="Assign a user-friendly name to the output file. Do not include the extension.",
    )

    # Future work
    # group = args.add_mutually_exclusive_group()
    # group.add_argument('--weeks', type=int, default=None)
    # group.add_argument('--months', type=int, default=None)
    return parser


def main():
    """Main cli function."""
    parser = get_parser()
    args = parser.parse_args()

    c = CensysBigQuery(user_filename=args.output)
    c.query_censys(args.query, output_type=args.format)


if __name__ == "__main__":  # pragma: no cover
    main()
