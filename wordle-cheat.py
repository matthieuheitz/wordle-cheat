#!/usr/bin/env python3

import numpy as np
import itertools

# Get list of words
fd = open('words_freebsd.txt', 'r')
lines = fd.readlines()
words = [grp.split('\n')[0] for grp in lines]

# Number of letters in each word
K = 5
# Set length: number of words in the set: 2 for pairs of words
S = 2

most_common = True  # Find most or least common letters


# Filter words:
# - non-capitalized (not proper nouns)
# - K letters
wordsK = [w for w in words if w[0].islower() and len(w) == K]
# - no double letters
# wordsK = [w for w in words if w[0].islower() and len(w) == K and len(set(w)) == K]

# This strategy relies on the assumption that the priority is to find all letters that are in the word.
# Another strategy would be to say that knowing the letters is not discriminative enough, so it would be
# better to focus on letters that appear less often.



# Compute letter frequency
alphabet = np.array(list("abcdefghijklmnopqrstuvwxyz"))
allwordsK = ''.join(wordsK)
lf = [allwordsK.count(l) for l in alphabet]

# Get the S*L most common letters
# cl = np.array(['e', 'a', 'r', 't', 'o', 'i', 's', 'l', 'n', 'c'])
switch_order = -1 if most_common else 1
cl = alphabet[np.argsort(lf)[::switch_order]][:S*K]
print("The %d most common letters in %d-letter words are:"%(S*K,K),cl)

# Find K-letter words that contain only the S*L most common letters
cl_w = np.array([w for w in wordsK if np.all([l in cl for l in w])])

# Find S-word sets of K-letter words that contain all S*L most common letters
cl_ws = np.array([ws for ws in itertools.combinations(cl_w, S) if set(''.join(ws)) == set(cl)])

print("Keeping words that only contain these most common letters (CL words)")

# Score pairs according to commonality of their letter positions
# Compute frequency of letter positions: letter x position
lpf = np.array([[np.count_nonzero([w[i] == l for w in wordsK]) for i in range(K)] for l in alphabet])
# Compute the letter-position-commonality (LPC) score of a word
word_lpf_score = lambda w: sum([lpf[ord(l)-97,i] for i,l in enumerate(w)])
word_lpf_score_by_letter = lambda w: [lpf[ord(l)-97,i] for i,l in enumerate(w)]

# Rank words by LPC score:
w_lpfs = [word_lpf_score(w) for w in cl_w]
w_lpfs_ranked = np.sort(w_lpfs)[::-1]
lpf_score_ranked_words = cl_w[np.argsort(w_lpfs)[::-1]]
print("Words with best letter-position-frequency (LPF) score (best 10):\n",np.vstack((lpf_score_ranked_words,w_lpfs_ranked)).T[:10])

# Compute LPC scores of all words in word sets
wws_lpfs = np.array([[word_lpf_score(w) for w in ws] for ws in cl_ws])

# Order words by LPC score within each word set
wws_lpfs_ranked = np.sort(wws_lpfs,axis=1)[:,::-1]
cl_ws_o = np.array([sorted(ws,key=word_lpf_score)[::-1] for ws in cl_ws])
ws_and_lpfs = np.hstack((cl_ws_o,wws_lpfs_ranked))
print("%d-word sets and word LPC scores:\n"%S, ws_and_lpfs)



# Rank word sets by highest first word LPC score
order_lpf_lex = np.lexsort(wws_lpfs_ranked.T[::-1])[::-1]
ws_and_lpfs_lex = ws_and_lpfs[order_lpf_lex]
print("Rank word sets by lexicographic order of LPC score (best 10):\n", ws_and_lpfs_lex[:10])


# Rank word sets by the sum of LPC scores of words in the set
aws_lpfs = [sum([word_lpf_score(w) for w in ws]) for ws in cl_ws]
aws_lpfs_ranked = np.sort(aws_lpfs)[::-1]
lpf_score_ranked_words = cl_ws[np.argsort(aws_lpfs)[::-1]]
ws_and_lpfs_sum = np.vstack((lpf_score_ranked_words.T,aws_lpfs_ranked)).T
print("Rank word sets by sum of LPC score (best 10):\n",ws_and_lpfs_sum[:10])




# Most

