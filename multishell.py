#!/usr/bin/env python3

import argparse
import os
import subprocess


def exec_command(command, directories, keep_executing, verbose):
    old_pwd = os.getcwd()
    for directory in directories:
        os.chdir(directory)
        result = subprocess.run(command, capture_output=True, shell=True)

        successful = result.returncode == 0
        print_output(
            successful,
            directory,
            result.stdout,
            result.stderr,
            result.returncode,
            verbose,
        )

        os.chdir(old_pwd)

        if not successful and not keep_executing:
            return


def format_stream(name, contents):
    return f"{name}: '{contents.decode().rstrip()}'" if contents else f"{name}: (None)"


def get_directories(args):
    directories = []

    if args.all:
        for i in sorted(os.listdir()):
            if os.path.isdir(i):
                directories.append(i)

    if args.directories:
        directories.extend(args.directories.split(","))

    if args.file:
        with open(args.file, "r") as dirs_file:
            directories.extend(dirs_file.readlines())

    return [x.rstrip() for x in directories]


def main(args):
    directories = get_directories(args)
    if len(directories) == 0:
        raise ValueError("No directories!")

    if args.batch_file:
        return run_script(
            directories, args.batch_file, args.keep_executing, args.verbose
        )

    done = False
    while not done:
        try:
            command = input("multishell$ ")
            exec_command(command, directories, args.keep_executing, args.verbose)
        except (EOFError, KeyboardInterrupt):
            print("Quit")
            done = True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive shell to run commands in multiple directories",
    )

    parser.add_argument(
        "-a",
        "--all",
        action="store_true",
        help="Add all directories in the currect path",
    )
    parser.add_argument(
        "-b",
        "--batch-file",
        help="Execute commands from this file (one command per line).",
    )
    parser.add_argument(
        "-c",
        "--continue",
        action="store_true",
        dest="keep_executing",
        help="Continue executing in spite of failures.",
    )
    parser.add_argument(
        "-d", "--directories", help="List of comma-separated directories.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File containing a list of directories, one per line.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Show output from successful commands.",
    )

    return parser.parse_args()


def print_output(successful, directory, stdout, stderr, returncode, verbose):
    output = []

    if successful:
        output.append("✔ ")
        output.append(directory)
        if verbose:
            output.append("-")
            output.append(format_stream("stdout", stdout))
            output.append(format_stream("stderr", stderr))
    else:
        output.append("❌")
        output.append(directory)
        output.append("-")
        output.append(format_stream("stdout", stdout))
        output.append(format_stream("stderr", stderr))
        output.append(f"return code: {returncode}")

    print(" ".join(output))


def run_script(directories, batch_file, keep_executing, verbose):
    with open(batch_file, "r") as fp:
        lines = [x.rstrip() for x in fp.readlines()]
        if lines[0].startswith("#!"):
            lines.pop(0)

    for line in lines:
        print(f"🏃 {line}")
        exec_command(line, directories, keep_executing, verbose)


if __name__ == "__main__":
    main(parse_args())
