import json
import sys
from datetime import datetime

from pkg_resources import resource_filename

from ..support.saver import Saver
from ..support.site_reader import SiteReader
from .command import Command


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
        """ This is the entry point of the Scan command. First initialize the saving process and a
            site reader process for each site in the data.
        """
        try:
            # Start the saving process.
            saver = Saver(args=self.args)
            saver.start()
            # Start the site reader processes
            site_readers = []
            for site in self.data["sites"]:
                site_reader = SiteReader(args=self.args,
                                         site_data=site,
                                         settings=self.settings,
                                         company_data=self.data["companies"])
                site_reader.start()
                site_readers.append(site_reader)
        except KeyboardInterrupt:
            for site_reader in site_readers:
                site_reader.terminate()
                site_reader.join()
            saver.queue.put({"post type":"quit"})
            saver.join()
            sys.exit(1)

    def print_state(self):
        running_time = (datetime.now()-self.start_time)
        days, seconds = running_time.days, running_time.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        self.iterations += 1
        self.log("|¯Scans:        {}".format(self.iterations))
        self.log("| Running time: {} {:02d}:{:02d}:{:02d}".format(days, hours, minutes, seconds))
        self.log("|_New articles: {}".format(self.new_articles))
