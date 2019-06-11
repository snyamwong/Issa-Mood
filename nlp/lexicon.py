"""
Using Association Approach
1. Go through the song lyrics sentence by sentence
2. Clean each string, from plural to singular, remove apostrophe, lowercase the string

Using Intensity Approach
"""

filepath = '../NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'

import pandas as pd

class Lexicon:
    def __init__(self):
        self.df = pd.read_csv(filepath, names = ['word', 'emotion', 'association'], skiprows = 1, sep = '	')

    def wordAssociation(self, word):
        return self.df[(lexicon.df.word == word) & (lexicon.df.association == 1)].emotion.tolist()

lexicon = Lexicon()
