# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field
from scrapy.contrib.djangoitem import DjangoItem
from magnet.models import Magnet

class EzinearticlesItem(Item):
    title = Field()
    content = Field()
    excerpt = Field()
    tag = Field()
    category = Field()


class EzinearticlesLinkItem(Item):
    link = Field()
    summary = Field()

class CaoLiuItem(Item):
    title = Field()
    content = Field()
    sid = Field()

class MagnetItem(DjangoItem):
    django_model = Magnet
