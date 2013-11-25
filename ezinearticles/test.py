# -*- coding: utf-8 -*-
__author__ = 'andyz'
import re
if __name__ == '__main__':
    url = 'http://184.154.128.243/htm_data/16/1311/974159.html'
    page_id_reg = re.compile(r'/(\d+)\.html')
    m = page_id_reg.findall(url)
    if m:
        print m[0]
    else:
        print 0