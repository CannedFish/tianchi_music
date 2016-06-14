# -*- coding: utf-8 -*-

class Progress(object):

    def __init__(self, total):
        self.total = total
        self.idx = 0

    def ins(self):
        self.idx += 1
        return self

    def show(self):
        print "%5d/%d" % (self.idx, self.total) 

