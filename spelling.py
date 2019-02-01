# http://norvig.com/spell-correct.html

# wont recognize if word is known
# edit distance = 2

import json
from collections import Counter

# # use_word_frequencies = 0

# # if use_word_frequencies == 1:
# #     with open('word_freqs.json') as f:
# #         WORDS = json.load(f)
# else:
with open('word_dict.json') as f:
    WORDS = json.load(f)

total = sum(WORDS.values())

def P(word, N=total):
    "Probability of `word`."
    if word not in WORDS or word == '':
        return 0
    else:
        return WORDS[word] / N

def correction(word, edit_dist = 1): 
    "Most probable spelling correction for word."
    return max(candidates(word, edit_dist), key=P)

def candidates(word, edit_dist): 
    "Generate possible spelling corrections for word."
    if edit_dist > 1:
        return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])
    else:
        return (known([word]) or known(edits1(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word): 
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))