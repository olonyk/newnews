#!/usr/bin/python3.5
"""
    Usage:
        newnews.py scan [-vl] [--settings=SCAN_SETTINGS] [--data=SCAN_DATA]
        newnews.py test
"""
from docopt import docopt
from src.scripts.commands.scan import Scan
from src.scripts.commands.test import Test

if __name__ == "__main__":
    args = docopt(__doc__)
    COMMAND = None
    if args["scan"]:
        args["name"] = "Scan"
        COMMAND = Scan(args)
    elif args["test"]:
        args["name"] = "Test module"
        COMMAND = Test(args)
    if COMMAND:
        COMMAND.run()