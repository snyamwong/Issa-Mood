"""
Python Script that cleans up song lyrics

# TODO: needs to clean out whatever Genius web scrapping returns
# TODO: improve lemmatize (analyzing the pos)
# TODO: 2-grams
# TODO: improve timing
# TODO: refactor code asap
# TODO: documentation oof
"""

import time
import nltk
import string
import inflection
import inflect

from collections import defaultdict
from lexicon import Lexicon
from inflection import singularize
from nltk.stem import WordNetLemmatizer
from nltk.corpus import stopwords
from textblob import TextBlob

"""
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
"""

def readSongLyrics(songpath):

    lyrics = []

    with open(songpath, 'r') as file:
        for line in file:
            lyrics.append(line)

    return lyrics

def getFilteredText(blob):

    stop_words = set(stopwords.words('english'))
    stop_words.add('ai') # ain't
    stop_words.add('wa') # wasn't
    p = inflect.engine()
    wnl = WordNetLemmatizer()

    result = []

    for sentence in blob:
        text = TextBlob(sentence)

        # cleaning the words
        words = [w.lower().translate(str.maketrans('', '', string.punctuation)) for w in text.words]

        # iT's pyThoNic
        filtered_text = ' '.join(wnl.lemmatize(str(w), pos='v') if(p.singular_noun(str(w))) else singularize(str(w)) for w in words if not w in stop_words)

        result.append(filtered_text)

    return result

def getLyricsEmotions(lyrics):

    emotion_dict = defaultdict(int)

    lexicon = Lexicon()

    for sentence in lyrics:
        for word in sentence.split():
            emotions = lexicon.wordAssociation(word)

            for emo in emotions:
                emotion_dict[emo] += 1

    return emotion_dict

if __name__ == '__main__':

    songpath = '../song/blessed.txt'

    lyrics = readSongLyrics(songpath)

    t0 = time.time()

    filtered_lyrics = getFilteredText(lyrics)

    t1 = time.time()

    print('timing for filtering lyrics:', t1 - t0)

    emotions = getLyricsEmotions(filtered_lyrics)

    print(emotions)

    """
    two_gram = filtered_sentence.ngrams(2)

    print(two_gram)
    """
