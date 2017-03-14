from random import randint
from random import choice
from random import uniform
from collections import namedtuple
from typing import List, Dict


_Options = namedtuple("Options",
                     ["vowels",
                      "consonants",
                      "max_initial_consonants",
                      "max_vowels",
                      "max_final_consonants",
                      "max_syllables",
                      "consonant_frequencies"])

# class Options:
#     def __init__(self, vowels, consonants, max_initial_consonants, max_vowels,
#                  max_final_consonants, max_syllables, consonant_frequencies):
#         self.vowels = vowels
#         self.consonants = consonants
#         self.max_initial_consonants = max_initial_consonants
#         self.max_vowels = max_vowels
#         self.max_final_consonants = max_final_consonants
#         self.max_syllables = max_syllables
#         self.consonant_frequencies = consonant_frequencies


class Options:
    def __init__(self, initial_consonant_probabilities, vowel_probabilities,
                 final_consonant_probabilities, syllable_count_probabilities,
                 initial_consonant_count_probabilities, vowel_count_probabilities,
                 final_consonant_count_probabilities):
        self.initial_consonant_probabilities = initial_consonant_probabilities
        self.vowel_probabilities = vowel_probabilities
        self.final_consonant_probabilities = final_consonant_probabilities
        self.syllable_count_probabilities = syllable_count_probabilities
        self.initial_consonant_count_probabilities = initial_consonant_count_probabilities
        self.vowel_count_probabilities = vowel_count_probabilities
        self.final_consonant_count_probabilities = final_consonant_count_probabilities

    def __repr__(self):
        return ("initial_consonant_probabilities={}\nvowel_probabilities={}\nfinal_consonant_probabilities={}\n" +
                "syllable_count_probabilities={}\ninitial_consonant_count_probabilities={}\n" +
                "vowel_count_probabilities={}\nfinal_consonant_count_probabilities={}").format(
            self.initial_consonant_probabilities,
            self.vowel_probabilities,
            self.final_consonant_probabilities,
            self.syllable_count_probabilities,
            self.initial_consonant_count_probabilities,
            self.vowel_count_probabilities,
            self.final_consonant_count_probabilities,
        )


START = '~'
END = '$'


def weighted_choice(choices):
    total = sum(w for c, w in choices)
    r = uniform(0, total)
    upto = 0
    for c, w in choices:
        if upto + w >= r:
            return c
        upto += w

    assert False


def equal_weights(l):
    weights = {}

    for item in l:
        weights[item] = [(i, 1) for i in l]
    return weights


def random_weights(l):
    weights = {}

    for item in l:
        weights[item] = [(i, uniform(0, 1)) for i in l]
    return weights


def random_chain_weights(items) -> Dict[str, List[List]]:
    weights = {}
    for item in items:
        weights[item] = [(_item, uniform(0, 1)) for _item in items]

    weights[START] = [[item, uniform(0, 1)] for item in items]

    return weights


def uniform_random_weights(min_value, max_value) -> List:
    probabilities = [[i, 1] for i in range(min_value, max_value+1)]
    return probabilities


def flatten(l):
    return [item for sublist in l for item in sublist]


def generate_word(options):
    num_syllables = weighted_choice(options.syllable_count_probabilities)

    syllables = [generate_syllable(options) for _ in range(num_syllables)]

    return "".join(flatten(syllables))


def generate_syllable(options: Options):
    syllable = [START]
    consonants = set(options.initial_consonant_probabilities.keys())
    vowels = set(options.vowel_probabilities.keys())

    num_init_consonants = weighted_choice(options.initial_consonant_count_probabilities)
    num_vowels = weighted_choice(options.vowel_count_probabilities)
    num_final_consonants = weighted_choice(options.final_consonant_count_probabilities)

    for _ in range(num_init_consonants):
        consonant = weighted_choice(options.initial_consonant_probabilities[syllable[-1]])
        syllable.append(consonant)

    for _ in range(num_vowels):
        if syllable[-1] in vowels:
            vowel = weighted_choice(options.vowel_probabilities[syllable[-1]])
            syllable.append(vowel)
        else:
            vowel = weighted_choice(options.vowel_probabilities[START])
            syllable.append(vowel)

    for _ in range(num_final_consonants):
        if syllable[-1] in consonants:
            consonant = weighted_choice(options.final_consonant_probabilities[syllable[-1]])
            syllable.append(consonant)
        else:
            consonant = weighted_choice(options.final_consonant_probabilities[START])
            syllable.append(consonant)

    syllable.append(END)

    return syllable[1:-1]


def generate_word_old(options):
    word = []

    for _ in range(randint(1, options.max_syllables)):
        num_initial_consonants = randint(0, options.max_initial_consonants)
        num_vowels = randint(1, options.max_vowels)
        num_final_consonants = randint(0, options.max_final_consonants)

        for _ in range(num_initial_consonants):
            if len(word) > 0 and word[-1] in options.consonants:
                next_consonant = weighted_choice(options.consonant_frequencies[word[-1]])
                word.append(next_consonant)
            else:
                word.append(choice(options.consonants))

        for _ in range(num_vowels):
            word.append(choice(options.vowels))

        for _ in range(num_final_consonants):
            if len(word) > 0 and word[-1] in options.consonants:
                next_consonant = weighted_choice(options.consonant_frequencies[word[-1]])
                word.append(next_consonant)
            else:
                word.append(choice(options.consonants))

    return "".join(word)


def random_options(vowels, consonants):
    vowel_counts = uniform_random_weights(1, 2)
    init_counts = uniform_random_weights(0, 2)
    syllables = uniform_random_weights(1, 4)
    final_counts = uniform_random_weights(0, 2)
    vowel_ps = random_chain_weights(vowels)
    final_c_ps = random_chain_weights(consonants)
    init_c_ps = random_chain_weights(consonants)

    options = Options(init_c_ps, vowel_ps, final_c_ps, syllables, init_counts, vowel_counts, final_counts)
    return options
