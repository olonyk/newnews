from multiprocessing import Process
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin
from urllib.request import urlopen

from bs4 import BeautifulSoup, SoupStrainer
from bs4.element import Comment

import requests

from ..commands.command import Command


class SiteReader(Process):
    def __init__(self, args=None, site_data=None, settings=None, company_data=None):
        super(SiteReader, self).__init__()
        self.site_data = site_data
        self.settings = settings
        self.company_data = company_data
        self.base_url = self.site_data["url"]
        args["name"] = self.site_data["name"]
        self.base_command = Command(args)
        self.visited_urls = []
        #self.log("Site reader for {} is initialized.".format(site_data["name"]))
    
    def run(self):
        """ Main function. First it finds all the links in the base url, their links and 
            recursively so on in the depth given in the settings. Then opens these urls and 
            searches for new articles about companies.
        """
        # Get a list of urls by recursive following links from the base url.
        urls = self.recursive_search([self.base_url], self.settings["search depth"])
        # Filter out the urls that have been visited before.
        nr_urls = len(urls)
        urls = list(set(urls)- set(self.visited_urls))
        self.visited_urls += urls
        self.base_command.log("Search resulted in {} urls, of which {} are new".format(nr_urls, len(urls)))
        # Find if the links mentions the companies considered.
        new_articles = self.find_mentions(urls)
        

    def recursive_search(self, urls, depth):
        """ Recursively find all links in the the pages found in urls. Returns a list of urls.
        """
        if depth == 0:
            return []
        new_urls = []
        for url in urls:
            if not url.startswith("http"):
                url = urljoin(self.base_url, url)
            try:
                with urlopen(url) as response:
                    for link in BeautifulSoup(response, "html.parser", parse_only=SoupStrainer('a')):
                        # Check the element contains a link.
                        if link.has_attr('href'):
                            # Don't include links to other sites.
                            if self.include(link["href"]):
                                if not link["href"].startswith("http"):
                                    link["href"] = urljoin(self.base_url, link["href"])
                                new_urls.append(link["href"])
            except (HTTPError, URLError, UnicodeEncodeError):
                pass

        new_urls = list(set(new_urls) - set(urls))
        return urls + self.recursive_search(new_urls, depth-1)

    def include(self, href):
        if (not href.startswith("http") or self.base_url in href) and not "mailto:" in href:
            return True
        return False

    def find_mentions(self, urls):
        """ Given a list of urls, check if they mention any of the companies in the data base.
        """
        new_articles = []
        for url in urls:
            try:
                with urlopen(url) as response:
                    soup = BeautifulSoup(response, 'html.parser')
                    texts = soup.findAll(text=True)
                    texts = [t.strip().lower() for t in filter(self.tag_visible, texts))]
                    for word in texts:
                        raise TODO
                        # Match the words in the text with the companies in the data

            except (HTTPError, URLError, UnicodeEncodeError):
                pass

    def tag_visible(self, element):
        if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
            return False
        if isinstance(element, Comment):
            return False
        return True
