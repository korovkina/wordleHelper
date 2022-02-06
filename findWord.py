#!/usr/bin/python3

import configparser
import string
import re

config_path = 'config.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(config_path, encoding='UTF-8')

SAVE_PATH = CONFIG['general']['save_path']


def main():
    sample = input('Type 5-letter word replacing unknown letters with *. For example, audi*\n')
    sample = check_sample(sample)
    forbidden_letters = input('Type letters that must be ignored (with or without spaces)\n')
    forbidden_letters = check_forbidden_letters(sample, forbidden_letters)
    print_options(find_options(sample, forbidden_letters))


def check_sample(sample):
    if len(sample) != 5:
        print('Sorry, this program support 5-letter words only')
        raise NameError('Not a 5-letter word')
    allowed_symbols = ['*']
    allowed_symbols.extend(string.ascii_letters)
    for char in sample:
        if char not in allowed_symbols:
            raise NameError('Forbidden symbol')
    return sample.lower()


def check_forbidden_letters(sample, forbidden_letters):
    forbidden_letters = forbidden_letters.replace(' ', '').replace(',', '').lower()
    for char in forbidden_letters:
        if char not in string.ascii_letters:
            raise NameError('Forbidden symbol')
        if char in sample:
            print(f'Symbol {char} can not be part of sample {sample}')
            raise NameError('Sample contains forbidden symbol')
    return forbidden_letters


def find_options(sample, forbidden_letters):
    final_options = []
    pattern = sample.replace('*', '\w')
    words = read_words()
    raw_options = re.findall(pattern, words)
    for option in raw_options:
        if not [letter for letter in forbidden_letters if letter in option]:
            final_options.append(option)
    return final_options


def read_words():
    with open(SAVE_PATH) as f:
        words = f.read().replace('\n', ' ').lower()
    return words


def print_options(options):
    if not options:
        print('Sorry, no options were found :(')
    else:
        print('Here is your options:')
        print('\n'.join(options))


if __name__ == "__main__":
    main()
