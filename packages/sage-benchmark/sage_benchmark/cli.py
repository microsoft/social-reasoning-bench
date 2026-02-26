import sys

from sage_benchmark.calendar_scheduling.cli import main as calendar_main
from sage_benchmark.form_filling.cli import main as forms_main
from sage_benchmark.marketplace.cli import main as marketplace_main

SUBCOMMANDS = ("calendar", "forms", "marketplace")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SUBCOMMANDS:
        print(f"Usage: sagebench {{{','.join(SUBCOMMANDS)}}} [options]")
        sys.exit(1)

    subcommand = sys.argv[1]
    sys.argv = [f"sagebench {subcommand}"] + sys.argv[2:]

    if subcommand == "calendar":
        calendar_main()
    elif subcommand == "forms":
        forms_main()
    else:
        marketplace_main()
