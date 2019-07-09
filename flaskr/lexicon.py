"""
Lexicon module
"""

from nltk.corpus import stopwords
import pandas as pd

NRC_FILEPATH = 'lexicon/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'
BAD_WORD_FILEPATH = 'lexicon/bad-words.txt'

class Lexicon:
    """
    Class for all things related to a lexicon (stop words, NRC lexion, etc)
    """
    def __init__(self):
        columns = ['word', 'emotion', 'association']

        self.lex = pd.read_csv(NRC_FILEPATH, names=columns, skiprows=1, sep='	')

        self.curse = pd.read_fwf(BAD_WORD_FILEPATH, names=['word'], skiprows=1)

        self.stop_words = set(stopwords.words('english'))

        # words left over from lemmatize
        self.stop_words.add('ai') # ain't
        self.stop_words.add('wa') # wasn't
        self.stop_words.add('ca') # can't
        self.stop_words.add('wo') # won't
        self.stop_words.add('m')

    def word_association(self, words):
        """
        Given a word, return a list of associated emotions.
        """
        associated_emos = self.lex.loc[(self.lex['word'].isin(words)) & (self.lex.association == 1)]

        return associated_emos.groupby('emotion').sum()

    def is_stop_word(self, word):
        """
        Checks if the word is a stop_word
        """

        if (word.isdigit() or word in self.stop_words or (self.curse['word'] == word).any()):
        	return True

        return False
