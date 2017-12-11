import json
from multiprocessing import Process, Queue

import pika

from ..commands.command import Command


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

        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = connection.channel()
        self.channel.exchange_declare(exchange='saves',
                                exchange_type='fanout')
        result = self.channel.queue_declare(exclusive=True)
        queue_name = result.method.queue

        self.channel.queue_bind(exchange='saves',
                        queue=queue_name)
        self.channel.basic_consume(self.callback,
                              queue=queue_name,
                              no_ack=True)
        

    def run(self):
        """ Main loop pf the saver, read the next data in the queue, parse it and save it in the
            correct files. In the queue post there must be a "post type" key that determines which
            action that should be taken.
        """
        self.channel.start_consuming()

    def callback(self, _, method, properties, body):
        post = json.loads(body.decode('utf8'))
        if post["post type"] == "quit":
            self.base_command.log("Terminating")
            self.channel.stop_consuming()
        elif post["post type"] == "scan":
            self.base_command.log("Writing data from {}".format(post["site"]))
            self.save_scan(post)

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
                site["visited urls"] = site["visited urls"] + queue_post["visited urls"]
                break
        # Pass the information of how many new articles found to the scan class and trigger it to
        # print the current state.
        #if self.parent:
        #    self.parent.new_articles += queue_post["new articles"]
        #    self.parent.print_state()
        # Save the updated data file.
        with open(self.args["--data"], 'w') as jsonfile:
            #data = json.dumps(file_data, indent=4, sort_keys=True)
            json.dump(file_data, jsonfile)
