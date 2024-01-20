```python
class Cli()
```

This `Cli` class means to act like an `namespace` in C, its only
purpose is to make this script more organized. This class holds all
methods that are related to the command line interface, such as showing
information on the screen or interacting with the user...



```python
@staticmethod
def show(msg: str)
```

Simple function that replaces some special characters to their
respective color codes, like replacing an `[g]`, which means "green",
to `\033[32m` of the string, then printing it on the screen.

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

+ **row**: Is the list of strings that you want to format to be compatible
           with SQL syntax.

> [!NOTE]
> For an example: If you give an `["52", "Rice", "20.7", "TRUE"]` list, it
> will return a list that looks like `["52", "E'Rice'", "20.7", "TRUE"]`



```python
def get_query_string(file_path: str, dlmtr: str = ",") -> str
```

Open the specified file to format a SQL statement that inserts every
row values on the `.csv` file into the table that has the same name of the
`.csv` file. Also, it checks for erros when opening the file, if something
goes wrong, it will exit the script with status 1.

+ **file_path**: Path string to access the file contents;
+ **dlmtr**: This is `,` by default, but you can set a custom delimiter if
             your file is formatted in a different way.

