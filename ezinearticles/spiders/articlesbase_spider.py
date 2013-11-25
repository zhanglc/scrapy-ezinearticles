# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from ezinearticles.items import EzinearticlesItem


class ArticlesBaseSpider(CrawlSpider):
    crawl_num = 6
    name = "article_base"
    allowed_domains = ["www.articlesbase.com"]

    urls = ['http://www.articlesbase.com/health-articles/%s/']
    start_urls = [link % page_num for page_num in xrange(1, crawl_num) for link in urls]

    rules = [
        Rule(SgmlLinkExtractor(allow=(r'/health-articles/\d+/',),
                               restrict_xpaths='//div[@class="title"]/h3/a/@href'), follow=True,
             process_request='add_cookie'),
        Rule(SgmlLinkExtractor(allow=(r'/.*?\d+\.html', )), callback='parse_item', follow=True)
    ]

    def add_cookie(self, request):
        request.replace(cookies=[
            {},
        ])

    def parse_item(self, response):
        self.log(response.url)
        hxs = HtmlXPathSelector(response)
        item = EzinearticlesItem()
        item['title'] = hxs.select('//h1/text()').extract()
        item['content'] = hxs.select('//div[@class="post"]/p').extract()
        item['excerpt'] = hxs.select('//meta[@name="description"]/@content').extract()
        return item