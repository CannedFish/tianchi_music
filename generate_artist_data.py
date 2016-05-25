#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, sys

if len(sys.argv) != 3:
    print 'generate_artist_data $table_src $table_dst'
    sys.exit(1)

table_src, table_dst = sys.argv[1], sys.argv[2]
conn = sqlite3.connect('./Data/tianchi_music')
c = conn.cursor()

c.execute("drop table if exists %s" % table_dst)
c.execute("create table %s (artist_id text, play_times integer, ds text)" % table_dst)

for artist in c.execute("select distinct artist_id from mars_tianchi_songs"):
    sql = "select sum(t1.play_times), t1.ds " +\
            "from %s as t1 " % table_src +\
            "join mars_tianchi_songs as t2 " +\
            "on t1.song_id==t2.song_id " +\
            "where t2.artist_id=='%s' " % artist[0] +\
            "group by t1.ds"
    print sql
    c2 = conn.cursor()
    artist_datas = []
    for artist_data in c2.execute(sql):
        artist_datas.append(artist + artist_data)
    c2.executemany('insert into %s values (?, ?, ?)' % table_dst, artist_datas)

conn.commit()
conn.close()

