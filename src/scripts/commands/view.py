import json
import random
import tkinter as tk
from collections import Counter
from datetime import datetime
from tkinter import HORIZONTAL, E, IntVar, N, S, Tk, W, ttk

from pkg_resources import resource_filename

from pubnub.pnconfiguration import PNConfiguration
from pubnub.pubnub import PubNub

from ..support.view_frame import ViewFrame
from .command import Command
from ..support.pubnub_listener import PubNubListener

class View(Command):
    def __init__(self, args):
        super(View, self).__init__(args)

        # Read the settings file
        if not args["--settings"]:
            args["--settings"] = resource_filename("src.data", "default_scan_settings.json")
        self.settings = json.loads(self.read_file(args["--settings"]))

        # Read the data file
        if not args["--data"]:
            args["--data"] = resource_filename("src.data", "default_scan_data.json")
        self.data = json.loads(self.read_file(args["--data"]))

        self.args = args
        
        self.signal = "save_msg"
 
        pnconfig = PNConfiguration()
        pnconfig.subscribe_key = "my_subkey"
        pnconfig.publish_key = "my_pubkey"
        pnconfig.ssl = False
        self.pubnub = PubNub(pnconfig)
        self.pubnub.add_listener(PubNubListener())
        self.pubnub.subscribe().channels('my_channel').execute()

        self.log("Initialized")

    def _callback(self, message, channel):
        self.log("A message: '{}' was recieved in channel: {}".format(message, channel))

    def run(self):
        # Create a list of plot frames in the format: [(string, frame), (string, frame), ...]
        plot_companies = []
        # Iterate through the list of companies.
        for company in self.data["companies"]:
            # Check if the company has at least one sighting.
            if "sightings" in company.keys():
                if len(company["sightings"]) > 1:
                    plot_companies.append(company)
        if plot_companies:
            main_root=tk.Tk()
            ViewFrame(master=main_root, company_data=plot_companies).pack(side="top", fill="both", expand=True)
            while True:
                try:
                    main_root.mainloop()
                    break
                except UnicodeDecodeError:
                    pass
        else:
            self.log("No data to view.")

    
        

# [{"site": "Aff\u00e4rsv\u00e4rlden", "datetime": "2017-11-21 10:48:35", "url": "https://www.affarsvarlden.se/bors-ekonominyheter/h-m-tappar-pa-borsen-6884635"}]
# {"name": "H&M", "sightings": [{"site": "Aff\u00e4rsv\u00e4rlden", "datetime": "2017-11-21 10:48:35", "url": "https://www.affarsvarlden.se/bors-ekonominyheter/h-m-tappar-pa-borsen-6884635"}]}
