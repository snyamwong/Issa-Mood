"""
Using Association Approach
1. Go through the song lyrics sentence by sentence
2. Clean each string, from plural to singular, remove apostrophe, lowercase the string

Using Intensity Approach
"""

import pandas as pd

filepath = '../NRC-Emotion-Lexicon-v0.92/NRC-Emotion-Lexicon-Wordlevel-v0.92.txt'

df = pd.read_csv(filepath, names = ['word', 'emotion', 'association'], skiprows = 1, sep = '	')

print(df[df.word == 'anger'])
