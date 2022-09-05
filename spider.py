# This file contains core classes for the web crawler.
# Author: Kai Xu
# Date: 05/11/2016


from HTMLParser import HTMLParser   # for parsing HTML
from urlparse import urljoin        # for join two urls
from urllib2 import urlopen         # for GET request
from helper import clean, get_domain, valid, contain_static


class HTMLParser(HTMLParser):
    '''
    HTML parser to fetch urls and show assets
    '''

    def handle_starttag(self, tag, attrs):
        '''
        Override of the default function to handle <a> and ??? tags
        TODO: update these comments when assets handling is done
        '''
        for key, val in attrs:
            if key == "href":
                if contain_static(val):             # handle static files
                    print "-", val                  # show the static file
                elif tag == "a":                    # handle links
                    url = urljoin(self.url, val)    # append relative path to the root path
                    url = clean(url)                # clean up url
                    if valid(url, self.domain):
                        self.urls.append(url)       # append url to the return list
                else:
                    pass


    def run(self, url):
        '''
        Run the parser and return links in this page
        '''
        self.url = url                  # save root path
        self.domain = get_domain(url)   # get and save domain
        self.urls = []                  # init return list

        # Open the url and parse it
        # FIXME:
        # There will be potential error when some website handshake is unsuccessful due to the SSL.
        # This is temporarly fixed by ignoring such failure but it should be further investiagted.
        try:
            response = urlopen(url)                 # request and get response
            html = response.read().decode("utf-8")  # read and encode response; NOTE: decode is necessary for unicode
            self.feed(html)                         # parse the html file in string format
        except KeyboardInterrupt:                   # deal with Ctrl-C
            exit()
        except:
            print "Unexpected failure happens and the spider escapes."

        return self.urls


class Spider(object):
    def __init__(self):
        self.to_visit = []
        self.visited = set([])
        self.parser = HTMLParser()

    def crawl(self, target_url):
        target_url = clean(target_url)      # clean target_url
        self.to_visit.append(target_url)    # put target_url to to_visit list

        while len(self.to_visit) > 0:
            url = self.to_visit.pop(0)      # get next url
            print "The spider is visiting:", url
            urls = self.parser.run(url)     # parse the url
            self.visited.add(url)            # add this visited url to visited list

            # Add urls from the parser to to_visit lits
            # When they are not visited or already in the to_vist list
            for url in urls:
                if url not in self.visited and url not in self.to_visit:
                    self.to_visit.append(url)

        print "The spider has finished crawling the web at {url}".format(url=target_url)


if __name__ == "__main__":
    print "I don't like snakes. Don't python me directly."
