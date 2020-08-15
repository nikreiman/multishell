#!/usr/bin/env python3.8

import argparse
import os
import subprocess


def exec_command(command, directories, verbose):
    old_pwd = os.getcwd()
    for directory in directories:
        os.chdir(directory)
        result = subprocess.run(
            command,
            capture_output=True,
            shell=True,
        )

        successful = (result.returncode == 0)
        stderr = "(None)"
        if result.stderr:
            stderr = f"'{result.stderr.decode().rstrip()}'"
        stdout = "(None)"
        if result.stdout:
            stdout = f"'{result.stdout.decode().rstrip()}'"
        output = []

        if successful:
            output.append("✅")
            output.append(directory)
            if verbose:
                output.append(f"[stdout] {stdout}")
                output.append(f"[stderr] {stderr}")
        else:
            output.append("❌")
            output.append(directory)
            output.append(f"[stdout] {stdout}")
            output.append(f"[stderr] {stderr}")
            output.append(f"return code {result.returncode}")
        print(": ".join(output))

        os.chdir(old_pwd)


def get_directories(args):
    directories = []

    if args.directories:
        directories.extend(args.directories.split(","))

    if args.file:
        with open(args.file, 'r') as dirs_file:
            directories.extend(dirs_file.readlines())
    
    return [x.rstrip() for x in directories]


def main(args):
    directories = get_directories(args)
    if len(directories) == 0:
        raise ValueError("No directories!")

    done = False
    while not done:
        try:
            command = input("multishell$ ")
            exec_command(command, directories, args.verbose)
        except (EOFError, KeyboardInterrupt):
            print("Quit")
            done = True


def parse_args():
    parser = argparse.ArgumentParser(
        description="Interactive shell to run commands in multiple directories",
    )

    parser.add_argument(
        "-d",
        "--directories",
        help="List of comma-separated directories.",
    )
    parser.add_argument(
        "-f",
        "--file",
        help="File containing a list of directories, one per line.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="Show output from successful commands.",
    )

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
