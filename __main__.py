import sys
from time import time
import pathlib as path

start_time = time()
end_time = 'File'

def print_help():
    print("chname - Change the name of a directory recursively")
    print("Usage: chname [options]")
    print("Options:")
    print("\t--version, -v: Print the version number")
    print("\t--help, -h: Print this help message")
    print("\t--dir, -d: The directory to iterate through")
    print("\t--prefix, -p: The prefix to use before the (--start-at) index")
    print("\t--start-at, -s: The index to start at")


if __name__ == "__main__":
    ACCEPTED_ARGS = [
        "--version",
        "-v",
        "--help",
        "-h",
        "--dir",
        "-d",
        "--start-at",
        "-s",
    ]

    args = sys.argv[1:]
    count = 0

    start_at: int = int(1)
    directory: None | str = None
    prefix: None | str = None

    if len(args) == 0:
        print("No arguments provided \n")
        print_help()
        sys.exit(1)

    # for arg in args:
    # 	if (arg not in ACCEPTED_ARGS):
    # 		print("Invalid argument: " + arg)
    # 		sys.exit(1)

    if "--version" in args or "-v" in args:
        print("chname v0.0.1")
        sys.exit(0)

    if "--help" in args or "-h" in args:
        print_help()
        sys.exit(0)

    if "--dir" in args:
        i = args.index("--dir")
        directory = args[i + 1]

    if "--start-at" in args:
        i = args.index("--start-at")
        start_at = int(args[i + 1])

    if "--prefix" in args:
        i = args.index("--prefix")
        prefix = args[i + 1]

    for item in path.Path(directory).iterdir():
        if item.is_file():
            new_name = f"{prefix}_{start_at}{item.suffix}"
            new_path = item.parent / new_name

            if new_path.exists():
                print(f"Skipped: {item.name} => {new_name}")
                continue

            item.rename(new_path)
            print(f"Renamed: {item.name} => {new_name}")
            count += 1
            start_at += 1

    end_time = time()
    elapsed_time = round(end_time - start_time, 2)

    print(f"\nRenamed {count} files in {elapsed_time}s ✨")
    sys.exit(0)
