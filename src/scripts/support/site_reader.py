from ..commands.command import Command
from multiprocessing import Process
class SiteReader(Command, Process):
    def __init__(self, args=None, site_data=None, settings=None, company_data=None):
        super(SiteReader, self).__init__(args)
        self.log("Site reader for {} is initialized.".format(site_data["name"]))
    
    def run(self):
        print("d")