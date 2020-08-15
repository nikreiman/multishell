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

        print_output(
            result.returncode == 0,
            directory,
            result.stdout,
            result.stderr,
            result.returncode,
            verbose,
        )
        os.chdir(old_pwd)


def format_stream(name, contents):
    return f"{name}: '{contents.decode().rstrip()}'" if contents else f"{name}: (None)"


def print_output(successful, directory, stdout, stderr, returncode, verbose):
    output = []

    if successful:
        output.append("✅")
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


def get_directories(args):
    directories = []

    if args.all:
        for i in sorted(os.listdir()):
            if os.path.isdir(i):
                directories.append(i)

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

    if args.script:
        return run_script(directories, args.script, args.verbose)

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
        "-a",
        "--all",
        action='store_true',
        help="Add all directories in the currect path",
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
        "-s",
        "--script",
        help="Execute commands from this script file.",
    )
    parser.add_argument(
        "-v",
        "--verbose",
        action='store_true',
        help="Show output from successful commands.",
    )

    return parser.parse_args()


def run_script(directories, script, verbose):
    with open(script, "r") as fp:
        lines = [x.rstrip() for x in fp.readlines()]
        if lines[0].startswith("#!"):
            lines.pop(0)

    for line in lines:
        print(f"🏃 {line}")
        exec_command(line, directories, verbose)


if __name__ == "__main__":
    main(parse_args())
