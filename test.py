#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sqlite3, sys, math

def calc_variance(real, train):
    def __calc(x, y):
        try:
            return (x[1]-y[1])*(x[1]-y[1])/y[1]/y[1]
        except Exception, e:
            return 0
    # lambda x,y: (x[1]-y[1])*(x[1]-y[1])/y[1]/y[1]
    return math.sqrt(reduce(lambda x,y: x+y, map(__calc, train, real))/len(real))

def calc_weight(real):
    return math.sqrt(reduce(lambda x,y: x+y, [a[1] for a in real]))

def calc_score(variances, weights):
    return reduce(lambda x,y: x+y, map(lambda x,y: (1-x)*y, variances, weights))

def do_test(conn, start, end):
    c = conn.cursor()

    c.execute("select distinct artist_id from artist_datas")
    artists = c.fetchall()

    c.execute("select distinct ds from artist_datas where ds>='%s' and ds<='%s'" % (start, end))
    dates = c.fetchall()

    variances = []
    weights = []
    for artist in artists:
        c.execute("select ds, play_times from artist_datas where artist_id=='%s' and ds>='%s' and ds<='%s'" % (artist[0], start, end))
        real_data = c.fetchall()
        c.execute("select ds, play_times from artist_prediction where artist_id=='%s' and ds>='%s' and ds<='%s'" % (artist[0], start, end))
        train_data = c.fetchall()

        variances.append(calc_variance(real_data, train_data))
        weights.append(calc_weight(real_data))

    score = calc_score(variances, weights)
    print score
    return score

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print "Usage: test $start $end"
        sys.exit(1)
    start, end = sys.argv[1], sys.argv[2]

    conn = sqlite3.connect('./Data/tianchi_music')
    do_test(conn, start, end)
    conn.close()

