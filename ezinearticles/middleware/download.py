# -*- coding: utf-8 -*-
import random
from scrapy import log
from ezinearticles.settings import USER_AGENT_LIST

class RandomProxyMiddleware(object):
    def __init__(self, settings):
        self.proxy_list = settings.get('PROXY_LIST')
        f = open(self.proxy_list)
        self.proxies = [l.strip().split('\t')[1] for l in f.readlines()]
        f.close()

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings)

    def process_request(self, request, spider):
        proxy = random.choice(self.proxies)
        log.msg('using proxy %s' % proxy)
        request.meta['proxy'] = proxy

    def process_exception(self, request, exception, spider):
        proxy = request.meta['proxy']
        log.msg('Removing failed proxy <%s>, %d proxies left' % (proxy, len(self.proxies)))
        try:
            self.proxies.remove(proxy)
        except ValueError:
            pass

class RandomUserAgentMiddleware(object):

    def process_request(self, request, spider):
        ua = random.choice(USER_AGENT_LIST)
        if ua:
            log.msg('using user agent %s' % ua)
            request.headers.setdefault('User-Agent', ua)