"""
Python Script that cleans up song lyrics

# TODO: needs to clean out whatever Genius web scrapping returns
# TODO: Singuarlize still needs some work
# TODO: 2-grams
"""

import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from textblob import TextBlob

"""
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('brown')
nltk.download('wordnet')
"""

stop_words = set(stopwords.words('english'))
stop_words.add('ai')

def readSongLyrics(songpath):

    lyrics = []

    with open(songpath, 'r') as file:
        for line in file:
            lyrics.append(line)

    return lyrics

def getFilteredText(blob):

    result = []

    for sentence in blob:
        text = TextBlob(sentence)

        # cleaning the words
        words = [w.singularize().lower().translate(str.maketrans('', '', string.punctuation)) for w in text.words]

        # filter out words
        filtered_text = [w for w in words if not w in stop_words]

        filtered_text = ' '.join(str(word) for word in filtered_text if len(word) > 0)

        result.append(filtered_text)

    return result

if __name__ == '__main__':

    songpath = '../song/blessed.txt'

    lyrics = readSongLyrics(songpath)

    filtered_lyrics = getFilteredText(lyrics)

    print(filtered_lyrics)

    """
    two_gram = filtered_sentence.ngrams(2)

    print(two_gram)
    """
