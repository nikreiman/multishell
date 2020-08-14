#!/usr/bin/env python3

import argparse
import os
import subprocess


def exec_command(command, directories):
    old_pwd = os.getcwd()
    for directory in directories:
        os.chdir(directory)
        result = ""
        try:
            subprocess.check_output(
                command,
                shell=True,
            )
            print(f"✅ {directory}: {result}")
        except subprocess.CalledProcessError as e:
            print(f"❌ {directory}: {result} ({e.returncode})")
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
            exec_command(command, directories)
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

    return parser.parse_args()


if __name__ == "__main__":
    main(parse_args())
