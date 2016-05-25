#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3

conn = sqlite3.connect('./Data/tianchi_music')
c = conn.cursor()

c.execute("drop table if exists music_datas")
c.execute("create table music_datas (song_id text, ds text, play_times integer)")

for music in c.execute("select song_id from mars_tianchi_songs"):
    sql = "select ds, sum(action_type) " +\
        "from mars_tianchi_user_actions " +\
        "where song_id=='%s' and action_type==1 " % music[0] +\
        "group by ds"
    print sql
    music_datas = []
    c2 = conn.cursor()
    for user_action in c2.execute(sql):
        music_datas.append(music + user_action)
    c2.executemany('insert into music_datas values (?, ?, ?)', music_datas)

conn.commit()
conn.close()

