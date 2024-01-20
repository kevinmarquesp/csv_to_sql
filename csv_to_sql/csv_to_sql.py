#!/usr/bin/env python3

from argparse import Namespace, ArgumentParser
import csv
import os
from sys import argv


COLOR_CODES = {
    "[b]": "\033[30m", "[r]": "\033[31m", "[g]": "\033[32m",
    "[y]": "\033[33m", "[b]": "\033[34m", "[m]": "\033[35m",
    "[c]": "\033[36m", "[w]": "\033[37m", "[/]": "\033[m"
}


def log(msg: str):
    r"""Simple function that replaces some special characters to their
    respective color codes, like replacing an `[g]`, which means "green", to
    `\033[32m` of the string, then printing it on the screen.

    + **msg**: The message that you want to show on the terminal output.
    """
    for key, value in COLOR_CODES.items():
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
                            and execute the generated SQL statement.")

    parser.add_argument("--host", "-H", type=str, help="Hostname of your\
                        database server.")
    parser.add_argument("--port", "-p", type=str, help="Port for the\
                        connection to your database server.")
    parser.add_argument("--user", "-u", type=str, help="Username to access\
                        the database tables.")
    parser.add_argument("--password", "-P", type=str, help="Password of your\
                        database user.")
    parser.add_argument("--db-name", "-d", type=str, help="The database\
                        this script should access once it's connected.")
    parser.add_argument("--print", action="store_true", help="If you don't\
                        want to connect to any database server, this option\
                        will make the code print the SQL query on the screen.\
                        You can then use it as you wish.")
    parser.add_argument("csv_files", type=str, nargs="+", help="List of `.csv`\
                        files that you want to use to generate the SQL query.")

    return parser.parse_args(args)


def join_list_format_sql(data: list[str]) -> str:
    r"""Utility function that joins every instance of a list with a `, `
    character, and put that string between `()`. Creating a string that is
    compatible with SQL syntax, you can use it to select columns in a table or
    to list values for each column.
    
    + **data**: List of strings that will be joined together.
    """
    return "(" + ", ".join(data) + ")"


def escape_sql_characters(sql_str: str) -> str:
    r"""Given a string, it will put a `\` character for each character that
    could cause some trouble in you SQL string. It's important if an user is
    called `Claire O’Connell` for an example, the `'` cound couse some syntax
    error -- also, it's important to avoid SQL injection.

    + **sql_str**: The string that you want to escape the characters;
    """
    ESCAPE_CHARS = ("'", '"', "\\", "%", "_", "/")
    escpaed_str = ""

    for char in sql_str:
        escpaed_str += char if char not in ESCAPE_CHARS else f"\\{char}"

    return escpaed_str


def format_sql_row(row: list[str]) -> list[str]:
    r"""The most complicated function, this function creates a list with
    strings that is compatible with SQL syntax. For an example: it replaces a
    "Foo" string for "E'Foo'" -- with special characters escaped -- and a "1"
    string to just "1". Maybe you'll need to check the test cases or the source
    code in order to understand that function well...

    > [!NOTE]
    > For an example: If you give an `["52", "Rice", "20.7", "TRUE"]` list, it
    > will return a list that looks like `["52", "E'Rice'", "20.7", "TRUE"]`

    + **row**: Is the list of strings that you want to format to be compatible
               with SQL syntax.
    """
    row = row[:]  #uses a copy of the original list

    for key, value in enumerate(row):
        is_numeric = value.replace(".", "").replace(",", "").isnumeric()
        escaped_value = escape_sql_characters(value)

        if is_numeric or value.lower() in ("true", "false", "null"):
            row[key] = value.upper()
        else:
            row[key] = f"E'{escaped_value}'"

    return row


def get_sql_slices(file_path: str, dlmtr: str = ","):
    r"""Utility function that opens the file and parses the header and column
    values string slices that are compatible with the SQL syntax.
    + **file_path**: Path string to access the file contents;
    + **dlmtr**: This is `,` by default, but you can set a custom delimiter if
                 your file is formatted in a different way.
    """
    with open(file_path, "r", newline="") as file:
        file_reader = csv.reader(file, delimiter=dlmtr)

        header_data = next(file_reader)
        header_sql_slice = join_list_format_sql(header_data)
        values_sql_slices_list = []

        for row in file_reader:
            row_formated = format_sql_row(row)
            row_sql_slice = join_list_format_sql(row_formated)
            values_sql_slices_list.append(row_sql_slice)

        values_sql_slice = ', '.join(values_sql_slices_list)

    return (header_sql_slice, values_sql_slice)


def get_insert_query(file_path: str, dlmtr: str = ",") -> str:
    r"""Open the specified file to format a SQL statement that inserts every
    row values on the `.csv` file into the table that has the same name of the
    `.csv` file. Also, it checks for erros when opening the file, if something
    goes wrong, it will exit the script with status 1.

    + **file_path**: Path string to access the file contents;
    + **dlmtr**: This is `,` by default, but you can set a custom delimiter if
                 your file is formatted in a different way.
    """
    insert_query_template = "INSERT INTO {0} {1} VALUES {2};"

    try:
        base_name = os.path.basename(file_path)
        table_name = os.path.splitext(base_name)[0]  #remove the file extention

        header_sql_slice, values_sql_slice = get_sql_slices(file_path, dlmtr)

    except Exception as err:
        log(f"[r]error:[/] couldn't open the [c]{file_path}[/] file")
        log(f"[y]{err}[/]")
        exit(1)

    return insert_query_template.format(table_name, header_sql_slice,
                                        values_sql_slice)


def connect_and_send(host: str, port: int, user: str, password: str,
                     db_name: str, insert_query: str) -> None:
    r"""This is the most important function. By default, it uses the database
    authentication information provided in the command line arguments to
    connect to a PostgreSQL database and send that query. If you want this
    script to work with different databases, maybe you would like to edit the
    source code for that, and that's the function that you're looking for.
    
    + **host**: Hostname of your database server;
    + **port**: Port for the connection to your database server;
    + **user**: Username to access the database tables;
    + **password**: Password of your database user;
    + **db_name**: The database this script should access once it's connected;
    + **insert_query**: Query that this code generates by reading a `.csv`
                        file.
    """
    import psycopg2

    try:
        with psycopg2.connect(host=host, port=port, user=user,
                              password=password, dbname=db_name) as conn:
            with conn.cursor() as cur:
                cur.execute(insert_query)

    except Exception as err:
        log(f"[r]error:[/] could not connect to the specifyed database...")
        log(f"[y]{err}[/]")
        exit(1)



def main(args: list[str]) -> None:
    parsed_args = parse_arguments(args)

    for file_path in parsed_args.csv_files:
        log(f"[b]info:[/] dealing with [c]{file_path}[/]")

        insert_query = get_insert_query(file_path)

        if parsed_args.print:
            print(insert_query)
            break

        log("[b]info:[/] configured to send query to a database")

        connect_and_send(parsed_args.host, parsed_args.port, parsed_args.user,
                         parsed_args.password, parsed_args.db_name,
                         insert_query)

        log('[g]done[/]')


if __name__ == "__main__":
    main(argv[1:])  #jumps the first element (the file name) from argv
