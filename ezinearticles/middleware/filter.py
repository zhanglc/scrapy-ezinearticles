# -*- coding: utf-8 -*-

from scrapy.dupefilter import RFPDupeFilter, request_fingerprint
import os


class DuplicateFilter(RFPDupeFilter):

    def request_seen(self, request):
        fp = request.url
        if fp.find('?cat=') != -1 or fp.find('thread0806.php?fid=16&search=') != -1:
            return False
        if fp in self.fingerprints:
            return True
        self.fingerprints.add(fp)
        if self.file:
            self.file.write(fp + os.linesep)