from sys import exit, argv
from time import time
from pathlib import Path
from argparse import ArgumentParser

start_time = time()

def print_help():
    print(
        "pryfixer - A simple way to change all the files in a directory blazing fast ⚡️"
    )
    print("Usage: pryfixer [options]")
    print("Options:")
    print("\t-h, --help  Print this help message")
    print("\t-v, --version  Print the version number")
    print("\t-d, --dir  The directory to iterate through")
    print("\t-p, --prefix  The prefix to use before the (--begin) index")
    print("\t-b, --begin  The index to start at")


if __name__ == "__main__":
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--version", "-v", action="store_true")
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--dir", "-d", type=str, default=None, required=True)
    parser.add_argument("--prefix", "-p", type=str, default="File", required=False)
    parser.add_argument("--begin", "-b", type=int, default=1, required=False)

    args = parser.parse_args()

    count = 0

    begin: int = args.begin
    directory: str = args.dir
    prefix: str = args.prefix

    if len(argv[1:]) == 0:
        print("No arguments provided \n")
        print_help()
        exit(1)

    if args.version:
        print("Pryfixer v0.1.0 [ Python 3.10 ]")
        exit(0)

    if args.help:
        print_help()
        exit(0)

    for item in Path(directory).iterdir():
        if item.is_file():
            new_name = f"{prefix}_{begin}{item.suffix}"
            new_path = item.parent / new_name
            begin += 1

            if new_path.exists():
                print(f"Skipped: {item.name} => {new_name}")
                continue

            item.rename(new_path)
            print(f"Renamed: {item.name} => {new_name}")
            count += 1

    end_time = time()
    elapsed_time = round(end_time - start_time, 2)

    print(f"\nRenamed {count} files in {elapsed_time}s ✨")
    exit(0)
