import sys

from sage_data_gen.calendar_scheduling.cli import main as calendar_main

SUBCOMMANDS = ("calendar",)


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SUBCOMMANDS:
        print(f"Usage: sagegen {{{','.join(SUBCOMMANDS)}}} [options]")
        sys.exit(1)

    subcommand = sys.argv[1]
    sys.argv = [f"sagegen {subcommand}"] + sys.argv[2:]

    calendar_main()
