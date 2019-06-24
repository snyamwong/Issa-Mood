"""
Python class for handling all lexicon related functionalities
"""

import pandas as pd

FILEPATH = 'NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'

class Lexicon:
    """
    Class to look up words in the NRC Lexicon.
    """
    def __init__(self):
        """
        """
        columns = ['word', 'emotion', 'association']

        self.lex = pd.read_csv(FILEPATH, names=columns, skiprows=1, sep='	')

    def word_association(self, word):
        """
        Given a word, return a list of associated emotions.
        """
        return self.lex[(self.lex.word == word) & (self.lex.association == 1)].emotion.tolist()

    def __regex_word(self, word):
        """
        """
