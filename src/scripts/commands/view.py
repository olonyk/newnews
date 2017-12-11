import json
import random
import tkinter as tk
from collections import Counter
from datetime import datetime
from tkinter import HORIZONTAL, E, IntVar, N, S, Tk, W, ttk

from pkg_resources import resource_filename

import pika
import threading
from ..support.view_frame import ViewFrame
from .command import Command


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

        self.view_frame = None

        # Establish connection to the network, subscrib to log messages.
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='logs',
                                exchange_type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='logs',
                        queue=queue_name)
        self.channel.basic_consume(self._callback,
                              queue=queue_name,
                              no_ack=True)
        self.log("Initialized")

    def _callback(self, _, method, properties, body):
        if self.view_frame:
            self.view_frame.text_prompt.insert("{}\n".format(tk.INSERT,body.decode('utf8')))

        
    def run(self):
        mq_recieve_thread = threading.Thread(target=self.channel.start_consuming)
        mq_recieve_thread.start()
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
            self.view_frame = ViewFrame(master=main_root, company_data=plot_companies)
            self.view_frame.pack()
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
