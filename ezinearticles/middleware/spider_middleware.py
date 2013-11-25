# -*- coding: utf-8 -*-

from scrapy.http import Request
from scrapy import log
from ezinearticles.settings import VISITED_LINK_FILE


class IgnoreVisitedLinkMiddleware(object):
    def __init__(self):

        try:
            with open(VISITED_LINK_FILE, 'r') as f:
                self.visited_link = [line.strip for line in f.readlines()]
                f.close()
        except IOError:
            log.msg('there is no visited link file: %s ' % VISITED_LINK_FILE)
            self.visited_link = []


    def process_spider_output(self, response, result, spider):
        for x in result:
            if isinstance(x, Request):
                if len(self.visited_link) == 0 or x.url not in self.visited_link:
                    yield x
                else:
                    log.msg('the link %s is visited. ignore' % x.url)
            else:
                yield x

    def process_spider_input(self, response, spider):
        response_url = response.url
        if response_url.find('?cat=') == -1 or response_url.find('thread0806.php?fid=16&search=') == -1:
            with open(VISITED_LINK_FILE, 'a') as f:
                f.write(response_url + '\n')
            f.close()
