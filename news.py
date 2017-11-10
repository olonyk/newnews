#!/usr/bin/python3.5
"""
    Usage:
        newnews.py scan [-vl] [--settings=SCAN_SETTINGS] [--data=SCAN_DATA]
"""
from docopt import docopt
from src.scripts.commands.scan import Scan

if __name__ == "__main__":
    args = docopt(__doc__)
    COMMAND = None
    if args["scan"]:
        args["name"] = "Scan"
        COMMAND = Scan(args)
    if COMMAND:
        COMMAND.run()