import sys

from sage_data_gen.calendar_scheduling.cli import main as calendar_main
from sage_data_gen.form_filling.cli import main as form_filling_main
from sage_data_gen.marketplace.cli import main as marketplace_main

SUBCOMMANDS = ("calendar", "form-filling", "marketplace")


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in SUBCOMMANDS:
        print(f"Usage: sagegen {{{','.join(SUBCOMMANDS)}}} [options]")
        sys.exit(1)

    subcommand = sys.argv[1]
    sys.argv = [f"sagegen {subcommand}"] + sys.argv[2:]

    if subcommand == "calendar":
        calendar_main()
    elif subcommand == "form-filling":
        form_filling_main()
    elif subcommand == "marketplace":
        marketplace_main()
