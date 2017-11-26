from ..commands.command import Command
from multiprocessing import Process, Queue
import json
from pydispatch import dispatcher

class Saver(Process):
    """ This is a queue driven process that reads incoming data in the queue and saves it in the
        according files.
    """
    def __init__(self, args=None):
        """ Params:
            args =  {"-l":bool                  # Log
                     "-v":bool                  # Verbose
                     "--data": string           # The path to the file where to save the scan data
        """
        super(Saver, self).__init__()
        if args: 
            args["name"] = "Saver"
        self.base_command = Command(args)
        self.queue = Queue()
        self.args = args
        dispatcher.connect(self.handle_signal, signal="save_msg", sender=dispatcher.Any)

    def run(self):
        """ Main loop pf the saver, read the next data in the queue, parse it and save it in the
            correct files. In the queue post there must be a "post type" key that determines which
            action that should be taken.
        """
        while True:
            queue_post = self.queue.get()
            if queue_post["post type"] == "quit":
                self.base_command.log("Terminating")
                break
            elif queue_post["post type"] == "scan":
                self.save_scan(queue_post)

    def handle_signal(self, sender):
        """ Put a new message of the save_msg type in the saving queue.
        """
        self.queue.put(sender)

    def save_scan(self, queue_post):
        """ Save a scanning of a web site.
        """
        # Load data file
        file_data = json.loads(self.base_command.read_file(self.args["--data"]))
        # Add the new sightings
        file_data["companies"] = queue_post["company data"]
        # Find the site that the site reader crawled and add to the visided url post.
        for site in file_data["sites"]:
            if queue_post["site"] == site["name"]:
                site["visited urls"] = queue_post["visited urls"]
                break
        # Pass the information of how many new articles found to the scan class and trigger it to
        # print the current state.
        #if self.parent:
        #    self.parent.new_articles += queue_post["new articles"]
        #    self.parent.print_state()
        # Save the updated data file.
        with open(self.args["--data"], 'w') as jsonfile:
            json.dump(file_data, jsonfile)