"""
Python class for handling all lexicon related functionalities
"""

import pandas as pd

FILEPATH = 'NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'

class Lexicon:
    """
    Class to look up words in the NRC Lexicon, as well as all stop words
    """
    def __init__(self):
        """
        """
        columns = ['word', 'emotion', 'association']

        self.lex = pd.read_csv(FILEPATH, names=columns, skiprows=1, sep='	')

    def word_association(self, words):
        """
        Given a word, return a list of associated emotions.
        """
        associated_emos = self.lex.loc[(self.lex['word'].isin(words)) & (self.lex.association == 1)]

        return associated_emos.emotion.tolist()

    def is_stop_word(self, word):
        """
        Checks if the word is a stop_word

        Includes infanity (too much ambiguity, )
        """
