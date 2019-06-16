"""
Python Script that cleans up song lyrics

# TODO: needs to clean out whatever Genius web scrapping returns
# TODO: 2-grams
# TODO: improve timing
# TODO: documentation oof
# TODO: Text reduction to improve timing(?)

things you need to download
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
"""

import threading
import time
import statistics
import nltk
import string

from collections import defaultdict
from lexicon import Lexicon
from nltk.corpus import stopwords
from textblob import TextBlob

"""

"""
def readSongLyrics(songpath):

    # what if i make a TextBlob here then just append to it?

    lyrics = []

    with open(songpath, 'r') as file:
        for line in file:
            lyrics.append(line)

    #print('lyrics', lyrics)

    return lyrics

"""

"""
def filterLyrics(blob):

    stop_words = set(stopwords.words('english'))
    # words left over from lemmatize
    stop_words.add('ai') # ain't
    stop_words.add('wa') # wasn't
    stop_words.add('ca') # can't
    stop_words.add('wo') # won't
    stop_words.add('m')

    # genius tags
    stop_words.add('intro')
    stop_words.add('verse')
    stop_words.add('hook')
    stop_words.add('chorus')
    stop_words.add('prechorus')

    filtered_words = []

    for sentence in blob:
        text = TextBlob(sentence)

        words = []
        for w in text.words:
            w = w.lemmatize('n')
            w = w.lower()
            w = w.translate(str.maketrans('', '', string.punctuation))

            if(w not in stop_words and not w.isdigit()):
                words.append(w)

        if len(words) > 0:
            filtered_words.append(' '.join(w for w in words))

    #print('filtered_words', filtered_words)

    return filtered_words

"""

"""
def getLyricsEmotions(lyrics):

    emotion_dict = defaultdict(int)

    lexicon = Lexicon()

    # group by key
    for sentence in lyrics:
        t0 = time.time()
        for word in sentence.split():
            emotions = lexicon.wordAssociation(word)

            for emo in emotions:
                emotion_dict[emo] += 1

    # merge
    # emotion_count = defaultdict(int)

    return emotion_dict

if __name__ == '__main__':

    songpath = '../song/cold.txt'
    t0 = time.time()
    lyrics = readSongLyrics(songpath)
    t1 = time.time()
    print('timing for reading lyrics:', t1 - t0)

    t0 = time.time()
    filtered_lyrics = filterLyrics(lyrics)
    t1 = time.time()
    print('timing for filtering lyrics:', t1 - t0)

    t0 = time.time()
    emotions = getLyricsEmotions(filtered_lyrics)
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
