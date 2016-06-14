1. Run "generate_music_data.py" to collect data of songs which includes play_times, download_times and collected_times per day based song_id.
2. Run "generate_artist_data.py music_datas artists_datas" to generate play times of artists per day.
3. Run "ridge_reg_test.py" to generate predicted play times of songs per day in the future.
4. Run "generate_artist_data.py music_prediction artists_prediction" to generate predicted play times of artists per day between 20150701 and 20150830.
5. Run "test.py 20150701 20150830" to get the score of prediction about dedicated date duration.
