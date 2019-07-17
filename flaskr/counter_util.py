"""
A module for converting a Counter to a Dictionary (such function doesn't exist in Python yet).
"""


def counter_to_dict(counter):
    """
    Converts counter to dictionary, also replaces the numpy value to an int
    """
    dic = {}

    for key, value in counter.items():
        dic[key] = int(value)

    return dic
