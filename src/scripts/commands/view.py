import json
import random
import tkinter as tk
from collections import Counter
from datetime import datetime
from tkinter import ttk
from tkinter import Tk, IntVar, S, N, E, W, HORIZONTAL
from pkg_resources import resource_filename

from .command import Command
from ..support.view_frame import ViewFrame

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
