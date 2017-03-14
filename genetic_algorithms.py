from word_generator import generate_word
from word_generator import Options
from random import uniform
from random import choice
from typing import Dict, List
from collections import defaultdict


def chance(percent):
    return uniform(0, 1) < percent


def mutate(value, amount):
    if chance(.5):
        return min(value + amount, 1.0)
    else:
        return max(value - amount, 0.0)


def mutate_chains(old_probabilities: Dict, mutation_chance: float, amount: float):
    new_probabilities = defaultdict(list)
    for top_level_phoneme, chain_probabilities in old_probabilities.items():
        for phoneme, probability in chain_probabilities:
            if chance(mutation_chance):
                new_probabilities[top_level_phoneme].append([phoneme, mutate(probability, amount)])
            else:
                new_probabilities[top_level_phoneme].append([phoneme, probability])

    return new_probabilities


def mutate_counts(old_counts: List[List], mutation_chance: float, amount: float):
    new_counts = []
    for count, probability in old_counts:
        if chance(mutation_chance):
            new_counts.append([count, mutate(probability, amount)])
        else:
            new_counts.append([count, probability])

    return new_counts


def mutate_options(options, mutation_chance, amount):
    initial_consonant_probabilities = mutate_chains(options.initial_consonant_probabilities, mutation_chance, amount)
    vowel_probabilities = mutate_chains(options.vowel_probabilities, mutation_chance, amount)
    final_consonant_probabilities = mutate_chains(options.final_consonant_probabilities, mutation_chance, amount)
    syllable_count_probabilities = mutate_counts(options.syllable_count_probabilities, mutation_chance, amount)
    initial_consonant_count_probabilities = mutate_counts(options.initial_consonant_count_probabilities, mutation_chance, amount)
    vowel_count_probabilities = mutate_counts(options.vowel_count_probabilities, mutation_chance, amount)
    final_consonant_count_probabilities = mutate_counts(options.final_consonant_count_probabilities, mutation_chance, amount)

    return Options(initial_consonant_probabilities, vowel_probabilities, final_consonant_probabilities,
                   syllable_count_probabilities, initial_consonant_count_probabilities, vowel_count_probabilities,
                   final_consonant_count_probabilities)


def combine_chains(first: Dict, second: Dict):
    new_probabilities = defaultdict(list)
    for top_level_phoneme in first.keys():
        for i in range(len(first[top_level_phoneme])):
            choices = [
                first[top_level_phoneme][i],
                second[top_level_phoneme][i]
            ]
            new_probabilities[top_level_phoneme].append(choice(choices))

    return new_probabilities


def combine_counts(first: List, second: List):
    new_probabilities = []
    for i in range(len(first)):
        choices = [
            first[i],
            second[i]
        ]
        new_probabilities.append(choice(choices))

    return new_probabilities


def combine_options(first: Options, second: Options):
    return Options(
        combine_chains(first.initial_consonant_probabilities, second.initial_consonant_probabilities),
        combine_chains(first.vowel_probabilities, second.vowel_probabilities),
        combine_chains(first.final_consonant_probabilities, second.final_consonant_probabilities),
        combine_counts(first.syllable_count_probabilities, second.syllable_count_probabilities),
        combine_counts(first.initial_consonant_count_probabilities, second.initial_consonant_count_probabilities),
        combine_counts(first.vowel_count_probabilities, second.vowel_count_probabilities),
        combine_counts(first.final_consonant_count_probabilities, second.final_consonant_count_probabilities)
    )


def next_generation(population, winners: List[int], mutation_chance, amount):
    pool = [population[i] for i in winners]
    new_population = []

    for i in range(len(population)):
        first = mutate_options(choice(pool), mutation_chance, amount)
        second = mutate_options(choice(pool), mutation_chance, amount)
        new_population.append(combine_options(first, second))

    return new_population


def print_population(population):
    for i, options in enumerate(population):
        print("[{}]".format(i))
        for word in (generate_word(options) for _ in range(40)):
            print("    {}".format(word))
        print("")
