import sys

from sage_benchmark.calendar_scheduling.cli import main as calendar_main
from sage_benchmark.form_filling.cli import main as forms_main


def main():
    if len(sys.argv) < 2 or sys.argv[1] not in ("calendar", "forms"):
        print("Usage: sagebench {calendar,forms} [options]")
        sys.exit(1)

    subcommand = sys.argv[1]
    sys.argv = [f"sagebench {subcommand}"] + sys.argv[2:]

    if subcommand == "calendar":
        calendar_main()
    else:
        forms_main()
