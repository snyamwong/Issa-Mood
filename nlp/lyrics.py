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
import nltk
import string

from collections import defaultdict
from lexicon import Lexicon
from nltk.corpus import stopwords
from textblob import TextBlob

class Lyrics:
    def __init__(self):
        self.lexicon = Lexicon()

        self.stop_words = set(stopwords.words('english'))

        # words left over from lemmatize
        self.stop_words.add('ai') # ain't
        self.stop_words.add('wa') # wasn't
        self.stop_words.add('ca') # can't
        self.stop_words.add('wo') # won't
        self.stop_words.add('m')

    """

    """
    def readSongLyrics(self, songpath):

        lyrics = []

        with open(songpath, 'r') as file:
            for line in file:
                lyrics.append(line)

        return lyrics

    """

    """
    def filterLyrics(self, blob):

        filtered_lyrics = []

        for sentence in blob:
            text = TextBlob(sentence)

            words = []
            for w in text.words:
                # remove Genius tags here
                if ('[' in w):
                    pass

                w = w.lemmatize('n')
                w = w.lower()
                w = w.translate(str.maketrans('', '', string.punctuation))

                if(w not in self.stop_words and not w.isdigit()):
                    words.append(w)

            if len(words) > 0:
                filtered_lyrics.append(' '.join(w for w in words))

        return filtered_lyrics

    """

    """
    def getLyricsEmotions(self, lyrics):

        emotion_dict = defaultdict(int)

        for sentence in lyrics:
            for word in sentence.split():
                emotions = self.lexicon.wordAssociation(word)

                for emo in emotions:
                    emotion_dict[emo] += 1

        return emotion_dict
