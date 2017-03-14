from itertools import islice
from collections import defaultdict
from re import sub
from random import choice

def window(seq, n=2):
    """Returns a sliding window (of width n) over data from the iterable"
       s -> (s0,s1,...s[n-1]), (s1,s2,...,sn), ...
    """
    it = iter(seq)
    result = tuple(islice(it, n))
    if len(result) == n:
        yield result
    for elem in it:
        result = result[1:] + (elem,)
        yield result


def get_frequencies(corpus, chain_size):
    frequencies = defaultdict(list)
    for ngram in window(corpus, chain_size):
        prefix = ngram[:-1]

        frequencies[prefix].append(ngram[-1])

    return frequencies


def sanitize_input(corpus):
    corpus = corpus.lower()
    bad_chars = r"[^a-zA-Z ]"

    no_bad_chars = sub(bad_chars, "", corpus)

    collapsed_whitespace = sub(r"\s+", " ", no_bad_chars)

    return collapsed_whitespace


def generate_word(frequencies, max_length):
    starting_chains = [chain for chain in frequencies if chain[0] == ' ']

    new_word = list(choice(starting_chains))

    for i in range(5):
        new_word.append(choice(frequencies[tuple(new_word[-3:])]))

    return new_word


