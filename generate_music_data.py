#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3
from progress import Progress

conn = sqlite3.connect('./Data/tianchi_music')
c = conn.cursor()

c.execute("drop table if exists music_datas")
c.execute("create table music_datas (song_id text, ds text, play_times integer, download_times integer, collect_times integer)")

c.execute("select distinct ds from mars_tianchi_user_actions order by ds")
dates = c.fetchall()

c.execute("select song_id from mars_tianchi_songs")
songs = c.fetchall()
pro = Progress(len(songs))

def data_split(song_id, dataset):
    splited = [[], [], []]
    for data in dataset:
        splited[data[1] - 1].append(data)
    # print "splited:\n %s" % splited 
    reduced = [[], [], []]
    for i in range(3):
        for date in dates:
            tmp = [y[1] for y in filter(lambda x: x[0]==date[0], splited[i])]
            if len(tmp) == 0:
                reduced[i].append([date[0], 0])
                continue;
            reduced[i].append([date[0], reduce(lambda x,y: x+y, tmp)/(i+1)])
    # print "reduced:\n %s" % reduced
    merged = map(lambda x,y,z: (song_id, x[0], x[1], y[1], z[1]), reduced[0], reduced[1], reduced[2])
    return merged

for music in songs:
    sql = "select ds, action_type " +\
        "from mars_tianchi_user_actions " +\
        "where song_id=='%s' " % music[0]
    c2 = conn.cursor()
    music_datas = data_split(music[0], c2.execute(sql))
    # print "merged:\n %s" % music_datas
    c2.executemany('insert into music_datas values (?, ?, ?, ?, ?)', music_datas)
    pro.ins().show()

conn.commit()
conn.close()

