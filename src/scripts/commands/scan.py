from ..support.site_reader import SiteReader
import json
from .command import Command
from pprint import pprint
from pkg_resources import resource_filename
from pprint import pprint
import time
from datetime import datetime


class Scan(Command):
    def __init__(self, args):
        super(Scan, self).__init__(args)
        self.args = args

        # Read the settings file
        if not args["--settings"]:
            args["--settings"] = resource_filename("src.data", "default_scan_settings.json")
        self.settings = json.loads(self.read_file(args["--settings"]))

        # Read the data file
        if not args["--data"]:
            args["--data"] = resource_filename("src.data", "default_scan_data.json")
        self.data = json.loads(self.read_file(args["--data"]))

        # Initialize local variables
        self.iterations = 1
        self.start_time = datetime.now()
        self.new_articles = 0

    def run(self):
        print("Scan running")
        # Main loop
        while self.settings["loop"]:
            # Initialize the site readers
            site_readers = []
            for site in self.data["sites"]:
                if site["name"] == "DN ekonomi":
                    site_reader = SiteReader(args=self.args,
                                            site_data=site,
                                            settings=self.settings,
                                            company_data=self.data["companies"])
                    site_reader.start()
                    site_readers.append(site_reader)
            for site_reader in site_readers:
                site_reader.join()
            self.print_state()
            self.iterations += 1
            time.sleep(self.settings["loop interval sec"])
    
    def print_state(self):
        running_time = (datetime.now()-self.start_time)
        days, seconds = running_time.days, running_time.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        self.log("|¯Iteration:    {}".format(self.iterations))
        self.log("| Running time: {} {:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds))
        self.log("|_New articles: {}".format(self.new_articles))