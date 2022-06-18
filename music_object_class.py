import numpy as np
class MusicObject(object):

    def __init__(self, artist_id, full_track_list, lyrics, text):

        self.artist_name = input(text)
        self.artist_id = artist_id
        self.full_track_list = full_track_list
        self.lyrics = lyrics


    def calculate_mean_wordcount(self):
        word_counts = []
        mean_words = int(np.mean(word_counts))
        return mean_words