#!/usr/bin/env python
# -*- coding: utf-8 -*-

import matplotlib.pyplot as plt

def paint(data):
    plt.plot(data, 'ro')
    plt.ylabel('play times')
    # plt.xlabel('date')
    plt.show()

if __name__ == '__main__':
    import sys
    import sqlite3

    if len(sys.argv) != 3:
        print "Usage: show_in_plot [artist|song] $ID"
        sys.exit(1)

    if sys.argv[1] == 'artist':
        src_id = 'artist_id'
        tables = ['artist_datas', 'artist_prediction']
    else:
        src_id = 'song_id'
        tables = ['music_datas', 'music_prediction']
    id = sys.argv[2]
    conn = sqlite3.connect('./Data/tianchi_music')
    cu = conn.cursor()

    pt_datas = []
    for table in tables:
        for pt in cu.execute("select play_times from %s where %s=='%s'" % (table, src_id, id)):
            pt_datas.append(pt[0])

    paint(pt_datas)

