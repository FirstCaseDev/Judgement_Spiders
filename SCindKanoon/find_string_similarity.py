import string
import re

def compute_jaccard_sim(str_1, str_2):
    str_1_words = set(str_1.lower().strip().split())
    str_2_words = set(str_2.lower().strip().split())
    intersection = str_1_words & str_2_words
    union = str_1_words | str_2_words
    return len(intersection)/float(len(union))

# print(compute_jaccard_sim("Hello, I am Soumya", "My name is soumya"))
