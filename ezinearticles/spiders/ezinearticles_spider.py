# -*- coding: utf-8 -*-
from scrapy.spider import BaseSpider
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.selector import HtmlXPathSelector
from ezinearticles.items import EzinearticlesItem


class EzinearticlesSpider(CrawlSpider):
    crawl_num = 10
    name = "ezinearticles"
    allowed_domains = ["ezinearticles.com"]

    urls = ['http://ezinearticles.com/?cat=Health-and-Fitness:Hair-Loss&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Skin-Care&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Beauty&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Back-Pain&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Weight-Loss&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Womens-Issues&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Popular-Diets&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Sleep-Snoring&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Fitness-Equipment&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Drug-Abuse&page=%s',
            'http://ezinearticles.com/?cat=Health-and-Fitness:Anti-Aging&page=%s']

    start_urls = [link % page_num for page_num in xrange(1, crawl_num) for link in urls]

    rules = [
        #Rule(SgmlLinkExtractor(allow=(r'/\?cat=Health-and-Fitness:[^&]+&page=\d+',),
        #                       restrict_xpaths=('//a[@class="article-title-link"]/@href',)), follow=True),
        Rule(SgmlLinkExtractor(allow=(r'/\?[^&]+&id=\d+', )), callback='parse_item',
             follow=False)
    ]

    def parse_item(self, response):
        self.log(response.url)
        hxs = HtmlXPathSelector(response)
        item = EzinearticlesItem()
        item['title'] = "".join(hxs.select('//h1/text()').extract()).strip()
        item['content'] = "".join(hxs.select('//*[@id="article-content"]/p').extract())
        item['excerpt'] = "".join(hxs.select('//meta[@property="og:description"]/@content').extract())
        item['tag'] = "".join(hxs.select('//meta[@name="keywords"]/@content').extract())
        item['category'] = hxs.select('//meta[@property="og:article:section"]/@content').extract()
        return item
