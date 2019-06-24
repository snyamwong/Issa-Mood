"""
Python class that cleans up song lyrics

# TODO: 2-grams
# TODO: improve timing
# TODO: Text reduction to improve timing(?)

things you need to download
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
"""

from collections import defaultdict
import string
from textblob import TextBlob
from nltk.corpus import stopwords
from lexicon import Lexicon

class Lyrics:
    """
    Class for cleaning, and creating a dictionary of emotions for lyrics
    """
    def __init__(self):
        self.lexicon = Lexicon()

        self.stop_words = set(stopwords.words('english'))

        # words left over from lemmatize
        self.stop_words.add('ai') # ain't
        self.stop_words.add('wa') # wasn't
        self.stop_words.add('ca') # can't
        self.stop_words.add('wo') # won't
        self.stop_words.add('m')

        # add curse words here

    def filter_lyrics(self, blob):
        """
        Given a blob of lyrics, filter out unncessary words
        """
        filtered_lyrics = []

        for sentence in blob.split('\n'):
            text = TextBlob(sentence)
            words = []

            # ignore any Genius tags
            if '[' not in sentence:
                for word in text.words:
                    word = word.lemmatize('n')
                    word = word.lower()
                    word = word.translate(str.maketrans('', '', string.punctuation))

                    if(word not in self.stop_words and not word.isdigit()):
                        words.append(word)

                if words:
                    filtered_lyrics.append(words)

        return filtered_lyrics

    def get_lyrics_emotions(self, lyrics):
        """
        Given filtered lyrics, return a dictionary of emotions
        """
        emotion_dict = defaultdict(int)

        for sentence in lyrics:
            for word in sentence:
                emotions = self.lexicon.word_association(word)

                for emo in emotions:
                    emotion_dict[emo] += 1

        return emotion_dict

def read_song_lyrics_from_file(songpath):
    """
    For testing purposes, reads lyrics from a file
    """
    lyrics = []

    with open(songpath, 'r') as file:
        for line in file:
            lyrics.append(line)

    return lyrics
