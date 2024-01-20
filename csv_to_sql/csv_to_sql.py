#!/usr/bin/env python3

from sys import argv
from argparse import Namespace, ArgumentParser
import csv
from typing import Iterator

## IDEA: let the user choose the delimeter character for the csv files

## TODO: the arguments can not handle the db connection yet
## TODO: fix the typos for the `parse_arguments/1` function docstring
## TODO: fix the typos for the `Cli.show/1` function docstring
## TODO: fix the typos for the `Cli` class docstring
## TODO: fix the typos for the `get_csv_file_reader/1` function docstring
## TODO: add the documentation for the arguments too


class Cli:
    """This `Cli` class means to act like an `namespace` in C, its only
    propurse is to make this script more organized. This class holds all
    methods that is related to the command line interface, such as showing
    information on the screen or interacting with the user...
    """
    clr_codes = {
        "[b]": "\033[30m", "[r]": "\033[31m", "[g]": "\033[32m",
        "[y]": "\033[33m", "[b]": "\033[34m", "[m]": "\033[35m",
        "[c]": "\033[36m", "[w]": "\033[37m", "[/]": "\033[m"
    }

    @staticmethod
    def show(msg: str):
        """Simple function that replaces some special characters to their
        respective color codes, like replacing an `[g]`, which means "green",
        to `\033[32m` of the string, then printing it on the screen.
        """
        for key, value in Cli.clr_codes.items():
            msg = msg.replace(key, value)
        print(msg)
        


def parse_arguments(args: list[str]) -> Namespace:
    """Given an list of arguments -- e.g. `['argument', '-o', '--option',
    'opttion_value']` -- this function puts everything toguether and return a
    `Namespace` object with all that arguments parsed to Python's types and
    easily accecible with the `parsed_args.option` notation.
    """
    parser = ArgumentParser(description="Simple Python script that reades a\
                            `.csv` file and generates a SQL statement that\
                            selects a table with the same name as the file and\
                            fill all rows with the file contents. Also, if\
                            you're using a PostgreSQL database, this command\
                            line tool allows you to connect to that database\
                            and execute the generated SQL database")

    parser.add_argument("csv_files", type=str, nargs="+", help="List of `.csv`\
                        files that you wanna use to generate the SQL query.")

    return parser.parse_args(args)


def get_csv_file_reader(file_path: str, dlmtr: str = ",") -> Iterator[list[str]]:
    """Try to open an `.csv` file, it this file doesn't exists or has an
    invalid path string, it will halt the whole program and show the error
    message with some adition information about that. If it not halts, it will
    just return the `csv.reader/1` iterator from the `csv` default library.
    + **file_path**: Path string to access the file contents;
    + **dlmtr**: This is `,` by default, but you can set a custom delimiter if
                 your file is formated in a different way.
    """
    try:
        with open(file_path, "r", newline="") as file:
            return csv.reader(file, delimiter=dlmtr)

    except Exception as err:
        Cli.show(f"[r]error:[/] could not open the [c]{file_path}[/] file specifyed")
        Cli.show(f"[y]{err}[/]")
        exit(1)


def main(args: list[str]) -> None:
    parsed_args = parse_arguments(args)

    for file_path in parsed_args.csv_files:
        file_reader = get_csv_file_reader(file_path)
        print(file_reader)


if __name__ == "__main__":
    main(argv[1:])  #jumps the first element (the file name) from argv
