# -*- coding: utf-8 -*-
import random
import re


class ArticleSpin(object):

    def __init__(self, glossary_file):
        super(ArticleSpin, self).__init__()
        self.glossary = dict()
        with open(glossary_file, 'r') as f:
            for line in f.readlines():
                vcs = line.strip().split("|")
                self.glossary.update([(vc, self._join(vc, vcs)) for vc in vcs])
            f.close()
        self.glossary.pop('')

    def _join(self, element, array):
        array_ = array[:]
        array_.remove(element)
        return '|'.join(array_)

    def _change_structure(self, article):
        article = article.strip()
        #TODO
        return article

    def spin(self, article):
        article = self._change_structure(article)
        for key, value in self.glossary.items():
            random_choice = random.choice(value.split("|"))
            if key in article:
                article = re.sub('\s' + key + '\s', ' {' + random_choice.replace(' ', '@@') + '} ', article, re.DOTALL)
            elif key.capitalize() in article:
                article = re.sub('\s{0,1}' + key.capitalize() + '\s',
                                 ' {' + random_choice.capitalize().replace(' ', '@@') + '} ',
                                 article, re.DOTALL)
                pass

        return article.replace('@@', ' ').replace('{', '').replace('}', '')