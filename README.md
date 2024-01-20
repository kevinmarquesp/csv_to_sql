```python
def log(msg: str)
```

Simple function that replaces some special characters to their
respective color codes, like replacing an `[g]`, which means "green", to
`\033[32m` of the string, then printing it on the screen.

+ **msg**: The message that you want to show on the terminal output.



```python
def parse_arguments(args: list[str]) -> Namespace
```

Given an list of arguments -- e.g. `['argument', '-o', '--option',
'optton_value']` -- this function puts everything together and returns a
`Namespace` object with all that arguments parsed to Python's types and
easily accessible with the `parsed_args.option` notation.

+ **args**: List of arguments that the user has specified, maybe you would
            like to use it with the `sys.argv` list to access the command
            line arguments.



```python
def join_list_format_sql(data: list[str]) -> str
```

Utility function that joins every instance of a list with a `, `
character, and put that string between `()`. Creating a string that is
compatible with SQL syntax, you can use it to select columns in a table or
to list values for each column.

+ **data**: List of strings that will be joined together.



```python
def escape_sql_characters(sql_str: str) -> str
```

Given a string, it will put a `\` character for each character that
could cause some trouble in you SQL string. It's important if an user is
called `Claire O’Connell` for an example, the `'` cound couse some syntax
error -- also, it's important to avoid SQL injection.

+ **sql_str**: The string that you want to escape the characters;



```python
def format_sql_row(row: list[str]) -> list[str]
```

The most complicated function, this function creates a list with
strings that is compatible with SQL syntax. For an example: it replaces a
"Foo" string for "E'Foo'" -- with special characters escaped -- and a "1"
string to just "1". Maybe you'll need to check the test cases or the source
code in order to understand that function well...

> [!NOTE]
> For an example: If you give an `["52", "Rice", "20.7", "TRUE"]` list, it
> will return a list that looks like `["52", "E'Rice'", "20.7", "TRUE"]`

+ **row**: Is the list of strings that you want to format to be compatible
           with SQL syntax.



```python
def get_sql_slices(file_path: str, dlmtr: str = ",")
```

Utility function that opens the file and parses the header and column
values string slices that are compatible with the SQL syntax.
+ **file_path**: Path string to access the file contents;
+ **dlmtr**: This is `,` by default, but you can set a custom delimiter if
             your file is formatted in a different way.



```python
def get_insert_query(file_path: str, dlmtr: str = ",") -> str
```

Open the specified file to format a SQL statement that inserts every
row values on the `.csv` file into the table that has the same name of the
`.csv` file. Also, it checks for erros when opening the file, if something
goes wrong, it will exit the script with status 1.

+ **file_path**: Path string to access the file contents;
+ **dlmtr**: This is `,` by default, but you can set a custom delimiter if
             your file is formatted in a different way.



```python
def connect_and_send(host: str, port: int, user: str, password: str,
                     db_name: str, insert_query: str) -> None
```

This is the most important function. By default, it uses the database
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



```python
def main(args: list[str]) -> None
```

Main function that parses command line arguments, logs information,
generates SQL insert queries from CSV files, and sends them to a database.
The function works as follows:

1. Parses the command line arguments;
1. Iterates over each CSV file path in the parsed arguments;
1. Generates an SQL insert query for the current CSV file;
1. If the `print` flag is set in the parsed arguments, it prints the insert
   query and breaks the loop; and
1. Connects to the database and sends the insert query.

+ **args**: List of command line arguments.

