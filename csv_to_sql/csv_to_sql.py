#!/usr/bin/env python3

from sys import argv
from argparse import Namespace, ArgumentParser
import csv
from typing import Iterator

CsvReader = Iterator[list[str]]


class Cli:
    r"""This `Cli` class means to act like an `namespace` in C, its only
    purpose is to make this script more organized. This class holds all
    methods that are related to the command line interface, such as showing
    information on the screen or interacting with the user...
    """
    clr_codes = {
        "[b]": "\033[30m", "[r]": "\033[31m", "[g]": "\033[32m",
        "[y]": "\033[33m", "[b]": "\033[34m", "[m]": "\033[35m",
        "[c]": "\033[36m", "[w]": "\033[37m", "[/]": "\033[m"
    }

    @staticmethod
    def show(msg: str):
        r"""Simple function that replaces some special characters to their
        respective color codes, like replacing an `[g]`, which means "green",
        to `\033[32m` of the string, then printing it on the screen.

        + **msg**: The message that you want to show on the terminal output.
        """
        for key, value in Cli.clr_codes.items():
            msg = msg.replace(key, value)
        print(msg)
        


def parse_arguments(args: list[str]) -> Namespace:
    r"""Given an list of arguments -- e.g. `['argument', '-o', '--option',
    'optton_value']` -- this function puts everything together and returns a
    `Namespace` object with all that arguments parsed to Python's types and
    easily accessible with the `parsed_args.option` notation.

    + **args**: List of arguments that the user has specified, maybe you would
                like to use it with the `sys.argv` list to access the command
                line arguments.
    """
    parser = ArgumentParser(description="Simple Python script that reads a\
                            `.csv` file and generates a SQL statement that\
                            selects a table with the same name as the file and\
                            fills all rows with the file contents. Also, if\
                            you're using a PostgreSQL database, this command\
                            line tool allows you to connect to that database\
                            and execute the generated SQL statement")

    parser.add_argument("csv_files", type=str, nargs="+", help="List of `.csv`\
                        files that you want to use to generate the SQL query.")

    return parser.parse_args(args)


#todo: check for typos
def join_list_format_sql(data: list[str]) -> str:
    r"""Utility function that joins every instance of a list with a `, `
    character, and put that string betwenn `()`. Creating a string that is
    compatible with SQL syntax, you can use it to select columns in a table or
    to list values for each column.
    
    + **data**: List of strings that will be joined together.
    """
    return "(" + ", ".join(data) + ")"


#todo: check for typos
def get_query_string(file_path: str, dlmtr: str = ",") -> str:
    r"""Open the specified file to format a SQL statement that inserts every
    row vlues on the `.csv` file into the table that has the same name of the
    `.csv` file. Also, it checks for erros when opening the file, if something
    wen wrong, it will exit the script with status 1.

    + **file_path**: Path string to acess the file contents;
    + **dlmtr**: This is `,` by default, but you can set a custom delimiter if
                 your file is formated in a different way.
    """
    try:
        with open(file_path, "r", newline="") as file:
            file_reader = csv.reader(file, delimiter=dlmtr)
            header_data = next(file_reader)

            header_sql_slice = join_list_format_sql(header_data)
            Cli.show(f"[g]log:[/] {header_sql_slice}")

    except Exception as err:
        Cli.show(f"[r]error:[/] could not open the [c]{file_path}[/] file specified")
        Cli.show(f"[y]{err}[/]")

        exit(1)

    return "SELECT VERSION();"


def main(args: list[str]) -> None:
    parsed_args = parse_arguments(args)

    for file_path in parsed_args.csv_files:
        query_string = get_query_string(file_path)
        print(query_string)


if __name__ == "__main__":
    main(argv[1:])  #jumps the first element (the file name) from argv
