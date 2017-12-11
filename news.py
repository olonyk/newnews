#!/usr/bin/python3.5
"""
    Usage:
        newnews.py scan [-vl] [--settings=SCAN_SETTINGS] [--data=SCAN_DATA]
        newnews.py view [-vl] [--settings=SCAN_SETTINGS] [--data=SCAN_DATA]
        newnews.py test
        newnews.py send
"""
from docopt import docopt
from src.scripts.commands.scan import Scan
from src.scripts.commands.view import View

if __name__ == "__main__":
    args = docopt(__doc__)
    COMMAND = None
    if args["scan"]:
        args["name"] = "Scan"
        COMMAND = Scan(args)
    elif args["view"]:
        args["name"] = "View"
        COMMAND = View(args)
    if COMMAND:
        COMMAND.run()