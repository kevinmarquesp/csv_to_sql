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
def get_csv_file_reader(file_path: str,
                        dlmtr: str = ",") -> Iterator[list[str]]
```

Try to open an `.csv` file, if this file doesn't exist or has an
invalid path string, it will halt the whole program and show the error
message with some additional information about that. If it doesn't halt, it
will just return the `csv.reader/1` iterator from the `csv` default
library.

+ **file_path**: Path string to access the file contents;
+ **dlmtr**: This is `,` by default, but you can set a custom delimiter if
             your file is formated in a different way.

