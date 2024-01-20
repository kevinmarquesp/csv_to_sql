#!/usr/bin/env python3

from sys import argv
from argparse import Namespace, ArgumentParser

## TODO: the arguments can not handle the db connection yet
## TODO: fix the typos for the `parse_arguments/1` function


def parse_arguments(args: list[str]) -> Namespace:
    """Given an list of arguments -- e.g. `['argument', '-o', '--option',
    'opttion_value']` -- this function puts everything toguether and return a
    `Namespace` object with all that arguments parsed to Python's types and
    easily accecible with the `parsed_args.option` notation.
    """
    parser = ArgumentParser(description="Simple Python script that reades a\
                            `.csv` file and generates a SQL statement that\
                            creates a table with the same name and fill all\
                            rows with the file contents. Also, if you're using\
                            a PostgreSQL database, this command line tool\
                            allows you to connect to that database and execute\
                            the generated SQL database")

    parser.add_argument("csv_files", type=str, nargs="+", help="List of `.csv`\
                        files that you wanna use to generate the SQL query.")

    return parser.parse_args(args)


def main(args: list[str]) -> None:
    parsed_args = parse_arguments(args)
    print(parsed_args)


if __name__ == "__main__":
    main(argv[1:])  #jumps the first element (the file name) from argv
