# Ikhlaq Ahmad
# ixa190000
# N Grmas
import sys

# Dependencies
import nltk
import re
import os
import pickle
from nltk import word_tokenize


def text_process(raw_text):
    # remove new line char
    raw_text = re.sub('\n', '', raw_text)

    tokens = word_tokenize(raw_text)

    # create bigram and unigram list
    bigrams = nltk.ngrams(tokens, 2)
    unigrams = nltk.ngrams(tokens, 1)

    # build bigram and unigram dictionary
    bigram_dict = {}
    for bg in bigrams:
        if bg not in bigram_dict:
            bigram_dict[bg] = 1
        else:
            bigram_dict[bg] += 1

    unigram_dict = {}
    for ug in unigrams:
        if ug[0] not in unigram_dict:
            unigram_dict[ug[0]] = 1
        else:
            unigram_dict[ug[0]] += 1

    return unigram_dict, bigram_dict


def main(sys_args):

    # set path
    path = sys_args

    # change directory
    os.chdir(path)

    # text dictionary
    texts = {}

    # iterate through all file in the argument folder
    for file in os.listdir():
        if file.startswith("LangId.train"):
            file_path = f"{path}/{file}"
            with open(file, 'r') as f:
                texts[file] = f.read()

    # Change path to pickle directory
    k = "../Pickles"
    os.chdir(k)

    # process and pickle text
    for k, text in texts.items():

        # process text
        ug, bg = text_process(text)

        # pickle text
        with open(k + '_bg_dict.pickle', 'wb') as file:
            pickle.dump(bg, file)
        with open(k + '_ug_dict.pickle', 'wb') as file:
            pickle.dump(ug, file)


if __name__ == '__main__':
    main(sys.argv[1])
