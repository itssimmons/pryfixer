from sys import exit, argv
from time import time
from pathlib import Path
from argparse import ArgumentParser
from shutil import rmtree
from os import scandir

VERSION = "0.2.0"

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
    print("\t-b, --begin  The index to start at")
    print("\t-p, --prefix  The prefix to use before the (--begin) index")
    print(
        "\t--pad_start  Pad the name with zeros to the desired length at the beginning of the numbers section"
    )
    print(
        "\t--pad_end  Pad the name with zeros to the desired length at the end of the numbers section"
    )
    print(
        "\t--dump_sql  In the --dir directory, you are be given a sql file to dump the files to"
    )
    print(
        "\t--pkg  The package to use in the sql file (is necessary to be used with --dump_sql)"
    )


if __name__ == "__main__":
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--version", "-v", action="store_true")
    parser.add_argument("--help", "-h", action="store_true")
    parser.add_argument("--dir", "-d", default=None, required=False)
    parser.add_argument("--pkg", default="PACKAGE", required=False)
    parser.add_argument("--prefix", "-p", default="File", required=False)
    parser.add_argument("--begin", "-b", type=int, default=1, required=False)
    parser.add_argument("--pad_end", type=int, default=0, required=False)
    parser.add_argument("--pad_start", type=int, default=0, required=False)
    parser.add_argument("--dump_sql", action="store_true", required=False)

    args = parser.parse_args()

    count = 0

    begin: int = args.begin
    directory: str = args.dir
    prefix: str = args.prefix
    pad_start: int = args.pad_start
    pad_end: int = args.pad_end

    def generate_sql(name: str, package: str, begin: int, is_last: bool = False):
        file_dir = Path(f"{directory}/.dump")
        file_name = "insert_dump.sql"

        insert_head_sql = "insert into images (`id`, `imageUrl`, `language`, `createdAt`, `updatedAt`, `name`, `imageType`, `imageUuid`, `isNewTemplate`, `translator`, `resPhotoRoyaltyFree`, `resPhotoSource`, `resVecRoyaltyFree`, `resVecSource`, `resTypoRoyaltyFree`, `isPremium`, `production`, `deleted`) VALUES"

        insert_sql = f"(null, 'https://cdn.socialpiper.com/public-content/{name}', 'es', now(), now(), '{name}', 'jpg', '30221bef-6e63-11ef-917f-12019b8475fe', '1', '', '1', '{package}', '1', 'HA', '1', '0', '1', '0'),"

        if begin == args.begin:
            if file_dir.exists():
                rmtree(file_dir.absolute())
            file_dir.mkdir(parents=True, exist_ok=True, mode=0o755)
            with open(file_dir.absolute() / file_name, "x") as f:
                f.write(f"{insert_head_sql}\n\t{insert_sql}")
        else:
            with open(file_dir.absolute() / file_name, "a") as f:
                if not is_last:
                    f.write(f"\n\t{insert_sql}")
                else:
                    f.write(f"\n\t{insert_sql[:-1]}\n")

        pass

    if len(argv[1:]) == 0:
        print("No arguments provided \n")
        print_help()
        exit(1)

    if args.version:
        import sys
        print(
            f"Pryfixer v{VERSION} [ Python {sys.version_info.major}.{sys.version_info.minor} ]"
        )
        exit(0)

    if args.help:
        print_help()
        exit(0)

    if args.dir is None:
        print("No directory provided \n")
        print("Usage: pryfixer [options]")
        print("pryfixer --dir|-d <directory>")
        exit(1)

    destination_path = Path(directory)
    
    for item in destination_path.iterdir():
        if item.is_dir():
            continue

        if item.is_file():
            str_begin = str(begin)

            if pad_start > 0:
                str_begin = str_begin.rjust(pad_start, "0")
            if pad_end > 0:
                str_begin = str_begin.ljust(pad_end, "0")

            new_name = f"{prefix}_{str_begin}{item.suffix}"
            new_path = item.parent / new_name

            count += 1

            if args.dump_sql and args.pkg:
                count_files = sum(1 for entry in scandir(destination_path) if entry.is_file())
                generate_sql(
                    new_name, args.pkg, begin, is_last=(count == count_files)
                )

            begin += 1

            if new_path.exists():
                print(f"Skipped: {item.name} => {new_name}")
                continue

            item.rename(new_path)
            print(f"Renamed: {item.name} => {new_name}")

    end_time = time()
    elapsed_time = round(end_time - start_time, 2)

    print(f"\nRenamed {count} files in {elapsed_time}s ✨")
    exit(0)
