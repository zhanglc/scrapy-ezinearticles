# -*- coding: utf-8 -*-
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

from wordpress_xmlrpc import Client, WordPressPost
from wordpress_xmlrpc.methods.posts import NewPost
from ezinearticles.spin import ArticleSpin
from ezinearticles import settings
from scrapy.contrib.spidermiddleware.offsite import OffsiteMiddleware
from scrapy.contrib.spidermiddleware.referer import RefererMiddleware
from scrapy import log
import re
from scrapy.exceptions import DropItem
#import MySQLdb
from magnet.models import Magnet

class EzinearticlesPipeline(object):
    def __init__(self):
        super(EzinearticlesPipeline, self).__init__()
        self.wordpress = Client('http://www.aixs.me/xmlrpc.php', 'admin', '861122zlc')
        self.spin = ArticleSpin(settings.GLOSSARY_FILE)

    def process_item(self, item, spider):
        if spider.name != 'ezinearticles':
            return item
        cate_reg = re.compile(r'(Hair|Skin|Beauty|Back|Weight|Womens|Popular|Sleep|Fitness|Drug|Anti)', re.DOTALL)
        m = cate_reg.match(''.join(item['category']))
        if not m:
            raise DropItem('no the category i want')

        postid = self.wordpress.call(NewPost(self.buildPost(item)))
        log.msg('Ohhh... has post the %s' % item['title'])
        return item

    def buildPost(self, item):
        post = WordPressPost()
        post.title = self.spin.spin(item['title'])
        post.content = self.spin.spin(item['content'])
        post.excerpt = self.spin.spin(item['excerpt'])
        terms = []
        for x in item['tag'].split(','):
            x = x.strip()
            if len(x) != 0:
                terms.append(x)
        if len(terms) == 0:
            terms.append(item['category'])
        post.terms_names = {
            'post_tag': terms,
            'category': item['category'],
        }
        return post


class CaoLiuPipeline(object):
    def __init__(self):
        #self.conn = MySQLdb.connect(host="aixs-sg.cwgkgvo7k3p1.ap-southeast-1.rds.amazonaws.com",
        #                            user="root",
        #                            passwd="123qwert",
        #                            db="novel",
        #                            charset='utf8')
        self.filter = [u'举报贴', u'圖區', u'评分', u'公告', u'图床',
                       u'技术贴', u'广告贴', u'必读', u'举报贴', u'发贴前'
        ]

    def process_item(self, item, spider):
        if spider.name != 'caoliu':
            return item
        self.valid_item(item)

        if self.is_exist(item['sid']):
            raise DropItem('the topic %s is exist' % item['title'])

        return item

    def save(self, item):
        x = self.conn.cursor()
        try:
            sql = "INSERT INTO topic(sid,title,content,category,type) VALUES(%s,%s,%s,2,1)"
            x.execute(sql, (item['sid'], item['title'], item['content']))
            self.conn.commit()
        except :
            self.conn.rollback()
            raise DropItem('database error')

    def valid_item(self, item):

        if len(item['content']) == 0 or len(item['title']) == 0:
            raise DropItem('no content or title!')

        for x in self.filter:
            if x in item['title']:
                raise DropItem('common topic %s' % item['title'])


    def is_exist(self, page_id):
        x = self.conn.cursor()
        try:
            x.execute("""SELECT COUNT(1) FROM topic WHERE sid=%s LIMIT 1""", page_id)
            count = x.fetchone()[0]
            if count == 0:
                return False
            return True
        except :
            # print 'error name:', path
            return True

    def close_spider(self, spider):
        log.msg('spider %s is done!' % spider.name)
        self.conn.close()


class MagnetPipeline(object):

    def process_item(self, item, spider):
        if spider.name != 'magnet':
            return item

        if len(item['name']) == 0 or len(item['link']) == 0:
            raise DropItem('no name or link!')

        item.save()