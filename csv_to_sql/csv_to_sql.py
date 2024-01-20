#!/usr/bin/env python3

from sys import argv


def main(args: list[str]) -> None:
    print(args)


if __name__ == "__main__":
    main(argv[1:])  #jumps the first element (the file name) from argv
