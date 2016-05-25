#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('./Data/tianchi_music')
c = conn.cursor()

for ds in c.execute("select distinct ds from mars_tianchi_user_actions"):
    c2 = conn.cursor()
    c2.execute("select count(*) from artist_datas where ds=='%s'" % ds[0])
    ret = c2.fetchone()
    if ret[0] != 50:
        print "%s: %s" % (ds[0], ret[0])

