import time

from lyrics import Lyrics

if __name__ == '__main__':

    lyrics = Lyrics()

    songpath = '../song/dream_house.txt'
    t0 = time.time()
    song_lyrics = lyrics.readSongLyrics(songpath)
    t1 = time.time()
    print('timing for reading lyrics:', t1 - t0)

    t0 = time.time()
    filtered_lyrics = lyrics.filterLyrics(song_lyrics)
    t1 = time.time()
    print('timing for filtering lyrics:', t1 - t0)

    t0 = time.time()
    emotions = lyrics.getLyricsEmotions(filtered_lyrics)
    t1 = time.time()
    print('timing for getting emotions', t1 - t0)
    print(emotions)

    """
    thread = threading.Thread(target=getLyricsEmotions, args=(filtered_lyrics))
    thread.start()
    thread.join()
    """

    """
    two_gram = filtered_sentence.ngrams(2)

    print(two_gram)
    """
