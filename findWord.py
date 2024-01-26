#!/usr/bin/python3

import configparser
import string
import re

config_path = 'config.ini'
CONFIG = configparser.ConfigParser()
CONFIG.read(config_path, encoding='UTF-8')

SAVE_PATH = CONFIG['general']['save_path']


def main():
    sample = get_sample()
    forbidden_letters = get_forbidden_letters(sample)
    required_letters = get_required_letters()
    print_options(find_options(sample, forbidden_letters, required_letters))


def get_sample():
    sample = False
    while not sample:
        sample = input('Type 5-letter word replacing unknown letters with *. For example, audi*\n')
        sample = check_sample(sample)
    return sample


def check_sample(sample):
    if len(sample) != 5:
        print('Sorry, this program support 5-letter words only')
        return False
    allowed_symbols = ['*']
    allowed_symbols.extend(string.ascii_letters)
    for char in sample:
        if char not in allowed_symbols:
            print('Please, use only latin letters and *')
            return False
    return sample.lower()


def get_forbidden_letters(sample):
    forbidden_letters = False
    while not forbidden_letters:
        forbidden_letters = input('Type letters that must be ignored (with or without spaces)\n')
        print(forbidden_letters)
        forbidden_letters = check_forbidden_letters(sample, forbidden_letters)
    return forbidden_letters


def check_forbidden_letters(sample, forbidden_letters):
    forbidden_letters = forbidden_letters.replace(' ', '').replace(',', '').lower()
    for char in forbidden_letters:
        if char not in string.ascii_letters:
            print('Please, use only latin letters and *')
            return False
        if char in sample:
            print('Please, do not use symbols from sample')
            raise False
    return forbidden_letters


def get_required_letters():
    required_letters = False
    while not required_letters:
        required_letters = input('Ok, now what letters are definitely there?\n')
        required_letters = check_required_letters(required_letters)
    return required_letters


def check_required_letters(required_letters):
    required_letters = required_letters.replace(' ', '').replace(',', '').lower()
    for char in required_letters:
        if char not in string.ascii_letters:
            print('Please, use only latin letters and *')
            return False
    return required_letters


def find_options(sample, forbidden_letters, required_letters):
    final_options = []
    pattern = sample.replace('*', '\w')
    words = read_words()
    raw_options = re.findall(pattern, words)
    for option in raw_options:
        flag = False
        for letter in required_letters:
            if letter not in option:
                flag = True
        if not flag and not [letter for letter in forbidden_letters if letter in option]:
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
