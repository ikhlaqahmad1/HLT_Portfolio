"""
 ixa190000
 Ikhlaq Ahmad
 CS 4395 Human Language Technologies
 Homework: Word guessing game

"""

# imports

# Imports
import random
import re
import string
import sys

from collections import Counter

import nltk
from nltk import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Work lemmatizer object
wnl = WordNetLemmatizer()


"""
    preprocess():
        :param: Name of the file to be processed
        :returns: words' tokens, noun lemmas 
"""


def preprocess(file_name):

    # Opens and read the file in read mode
    file = open(file_name, 'r')
    data = file.read()

    # Removes punctuations, non-alpha chars, spaces
    text = data
    text = text.lower()
    text = re.sub(f"[{re.escape(string.punctuation)}]", "", text)
    text = " ".join(text.split())
    text = " ".join([w for w in text.split() if w.isalpha()])

    # Tokenizer
    tokens = word_tokenize(text)

    # Lexical Distribution percentage
    lexical_distribution = (len(set(tokens)) / len(tokens)) * 100
    print("Lexical diversity: " + f'{lexical_distribution: .2f}' + "%")

    # removes word < len(5) and stopwords 'english'
    filtered_text = [t for t in tokens if not t in stopwords.words("english") if len(t) > 5]
    new_tokens = word_tokenize(" ".join(filtered_text))

    # Lemmatize
    lemmas = [wnl.lemmatize(t) for t in new_tokens]

    # unique lemmas
    unique_lemmas = list(set(lemmas))

    # do pos-tags for lemmas
    tags = nltk.pos_tag(unique_lemmas)
    print("\nFirst 20 Pos-Tagged lemmas: {}".format(tags[:20]))

    tags = nltk.pos_tag(lemmas)

    # get noun lemmas only
    noun_pattern = "^NN"
    noun_lemmas = [l for l in tags if re.match(noun_pattern, l[-1])]
    print("\nNumber of tokens: {}. Number of nouns: {}".format(len(new_tokens), len(noun_lemmas)))

    file.close()

    return new_tokens, noun_lemmas


"""
    guessing_game()
        :param: list of 50 most common words
"""


def guessing_game(commons50):

    print("\nLet's play a word guessing game")
    score = 5
    cumulative_score = 0

    # pick randomly in top 50 commons
    pick = random.randint(0, 50)
    word = commons50[pick][0]
    holders = ['_'] * len(word)

    while True:
        print(' '.join(holders))
        guess = input("Guess a letter: ")

        if guess in word:
            if guess in holders:
                continue
            else:
                score += 1
                print('Right! Score is {}'.format(score))
                for i in range(len(word)):
                    if word[i] == guess:
                        holders[i] = guess
        elif guess != '!':
            score -= 1
            print('Sorry, guess again. Score is {}'.format(score))

        if score < 0 or guess == '!':
            print("End of game.")
            if cumulative_score == 0 and score > 0:
                cumulative_score += score
            print("Your cumulative score is {}".format(cumulative_score))
            break
        elif not '_' in holders:
            cumulative_score += score
            print('You solved it!')
            print("Current score is {}".format(score))
            print("Cumulative score is {}".format(cumulative_score))
            print("Guess another word")
            score = 5
            pick = random.randint(0, 50)
            word = commons50[pick][0]
            holders = ['_']*len(word)


"""
    main()
        :param: system args
"""


def main(sys_args):

    # Checks sys args
    num_of_args = len(sys_args)

    if num_of_args != 1:
        raise Exception("System Argument(s) invalid!")
    else:
        # File name to be processed
        file_name = ' '.join(sys_args)

        # preprocess function call
        processed_tokens, nouns = preprocess(file_name)

        # tokens dictionary
        token_dictionary = Counter(processed_tokens)
        token_dictionary = {k: v for k, v in token_dictionary.most_common()}

        # nouns dictionary
        nouns_dictionary = Counter(nouns)
        nouns_dictionary = {k: v for k, v in nouns_dictionary.most_common()}

        # 50 most common nouns
        common_50 = list(nouns_dictionary.keys())[:50]

        print("50 most common words: ")
        for key in common_50:
            print("Word \"{}\" has count: {}".format(key, nouns_dictionary[key]))

        # guessing_game call
        guessing_game(common_50)


# Main() call
if __name__ == "__main__":
    main(sys.argv[1:])
