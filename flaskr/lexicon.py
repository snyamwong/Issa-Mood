"""
Lexicon module
"""

from nltk.corpus import stopwords
from collections import Counter
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
        self.stop_words.add('nt')
        self.stop_words.add('m')

    def word_association(self, words):
        """
        # TODO: can most likely clean this up as a one dataframe call tbh
        Given a word, return a df of associated emotions.
        """
        negated_words = []
        true_words = []

        # this is to split up negated words into their own list, which will contain a '-'
        for word in words:
            if '-' in word:
                negated_words.append(word.split('-')[1])
            else:
                true_words.append(word)

        # taking all non associated emotions
        neg_emo = self.lex.loc[(self.lex['word'].isin(negated_words)) & (self.lex.association == 0)]

        neg_emo.loc[:, 'association'] = 1

        true_emo = self.lex.loc[(self.lex['word'].isin(true_words)) & (self.lex.association == 1)]

        concat_emos = pd.concat([neg_emo, true_emo])

        group_emo = concat_emos.groupby('emotion').sum()

        emotions = Counter(group_emo.T.to_dict('records')[0])

        return emotions

    def is_stop_word(self, word):
        """
        Checks if the word is a stop_word
        """

        if (word.isdigit() or word in self.stop_words or (self.curse['word'] == word).any()):
            return True

        return False
