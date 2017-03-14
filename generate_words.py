from word_generator import random_chain_weights
from word_generator import generate_word
from word_generator import Options
from word_generator import uniform_random_weights
import phonemes
from pprint import pprint


def main():
    vowel_counts = uniform_random_weights(1, 1)
    init_counts = uniform_random_weights(1, 1)
    syllables = uniform_random_weights(1, 4)
    final_counts = uniform_random_weights(0, 0)
    vowel_ps = random_chain_weights(phonemes.vowels)
    final_c_ps = random_chain_weights(phonemes.consonants)
    init_c_ps = random_chain_weights(phonemes.consonants)

    options = Options(init_c_ps, vowel_ps, final_c_ps, syllables, init_counts, vowel_counts, final_counts)
    words = [generate_word(options) for _ in range(10)]
    pprint(words)


if __name__ == '__main__':
    main()