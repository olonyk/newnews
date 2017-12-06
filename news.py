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
#from src.scripts.commands.test import Test
from src.scripts.commands.test import Sender

if __name__ == "__main__":
    args = docopt(__doc__)
    COMMAND = None
    if args["scan"]:
        args["name"] = "Scan"
        COMMAND = Scan(args)
    elif args["view"]:
        args["name"] = "View"
        COMMAND = View(args)
    elif args["send"]:
        args["name"] = "Sender module"
        COMMAND = Sender(args)
    if COMMAND:
        COMMAND.run()