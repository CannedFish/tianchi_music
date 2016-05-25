#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import sqlite3
from sklearn.linear_model import Ridge

conn = sqlite3.connect('./Data/tianchi_music')
cu = conn.cursor()

cu.execute('drop table if exists music_prediction')
cu.execute('create table music_prediction (song_id text, ds text, play_times integer)')

# maps date to integers
dates = range(20150301, 20150332) \
    + range(20150401, 20150431) \
    + range(20150501, 20150532) \
    + range(20150601, 20150631) \
    + range(20150701, 20150732) \
    + range(20150801, 20150831)
def pre_data_handle(raw):
    format_data = []
    idx, j = 0, 0
    for date in dates:
        if idx == len(raw) or date < int(raw[idx][0]):
            format_data.append((j, 0))
        else:
            format_data.append((j, raw[idx][1]))
            idx += 1
        j += 1
    return format_data

# return x[n_samples, n_features], y[n_features]
def generate_np_data(raw):
    pre = pre_data_handle(raw)
    arr = np.array(pre)
    X = np.reshape(arr[:, 0], (-1, 1)).astype(np.int)
    y = arr[:, 1].astype(np.int)
    return X, y

clf = Ridge(alpha=0.5)

cu.execute('select distinct song_id from music_datas')
song_ids = cu.fetchall()
total, idx = len(song_ids), 0
ds = range(20150901, 20150931) + range(20151001, 20151031)
X3 = np.reshape(np.array(range(183, 243)), (-1, 1)).astype(np.int)

for song_id in song_ids:
    # Model training
    sql = "select ds, play_times from music_datas " + \
        "where song_id=='%s'" % song_id # and ds<'20150701'
    cu2 = conn.cursor()
    cu2.execute(sql)
    ret = cu2.fetchall()
    # if len(ret) < 2:
        # print "%s: Not enough data for training!!" % song_id
        # idx += 1
        # continue
    X1, Y1 = generate_np_data(ret)
    clf.fit(X1, Y1)

    # Model test
    # sql = "select ds, play_times from music_datas " + \
        # "where song_id=='%s' and ds>='20150701'" % song_id
    # cu2.execute(sql)
    # ret = cu2.fetchall()
    # if len(ret) < 2:
        # print "%s: Not enough data for test!!" % song_id
        # continue
    # X2, y2 = generate_np_data(ret)
    # print "%s: %f" % (song_id, clf.score(X2, y2))

    # Predict
    Y3 = clf.predict(X3).tolist()
    predicts = []
    for (x, y) in zip(ds, Y3):
        if y < 0:
            y = 0
        predicts.append((song_id[0], x, round(y)))
    cu2.executemany('insert into music_prediction values (?, ?, ?)', predicts)

    # process
    idx += 1
    print "%5d/%d" % (idx, total) 

conn.commit()
conn.close()

