#!/usr/local/bin/python3

import sys
from rich.console import Console
from rich.table import Table
import argparse


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i : i + n]


def format(lines, cols=5, wrap=True):
    table = Table.grid(expand=True, padding=(0, 5, 0, 5))

    for i in range(cols):
        table.add_column(no_wrap=wrap)

    for line in chunks(lines, cols):
        table.add_row(*line)

    console = Console()
    console.print(table)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Format text as a columns")
    parser.add_argument("--cols", "-c", default=5, type=int)
    parser.add_argument(
        "--wrap", "-w", action=argparse.BooleanOptionalAction, default=False
    )
    parser.add_argument(
        "infile", nargs="?", type=argparse.FileType("r"), default=sys.stdin
    )
    args = parser.parse_args()
    with args.infile as infile:
        lines = infile.readlines()
    format(lines, args.cols, args.wrap)
