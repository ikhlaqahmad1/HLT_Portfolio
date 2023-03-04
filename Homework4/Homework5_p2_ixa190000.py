# Ikhlaq Ahmad

import os
import pickle
import Homework5_p1_ixa190000 as program1


def compute_prob(text, dicts):

    input_ug, input_bg = program1.text_process(text)

    # vocab size
    vocab_size = sum([len(d['ug']) for d in dicts.values()])

    probs = {}
    for lang, v in dicts.items():
        probs[lang] = 1
        bg_dict, ug_dict = v['bg'], v['ug']
        for bg, count in input_bg.items():

            # bigram count
            b = bg_dict[bg] if bg in bg_dict else 0

            # unigram count
            u = ug_dict[bg[0]] if bg[0] in ug_dict else 0

            # Laplace smoothing
            # raise the smoothing probability to the count of bigram
            probs[lang] *= ((b + 1) / (u + vocab_size)) ** count

    # sort probabilities to find the language with the highest probabilit
    lang = sorted(probs.items(), key=lambda x: x[1], reverse=True)
    return lang[0]


def main():

    # Change the directory to Pickles folder
    path = "Pickles"
    os.chdir(path)

    # nested dictionaries
    dicts = {'English': {}, 'French': {}, 'Italian': {}}

    # iterate through all pickle files
    for file in os.listdir():
        if file.endswith(".pickle"):
            file_path = f"{path}/{file}"
            with open(file, 'rb') as f:
                file = file.replace('.pickle', '').split('_')
                lang = file[0][13:]
                dicts[lang][file[1]] = pickle.load(f)

    # read test file
    with open("LangId.test") as f:
        tests = f.read()
        tests = tests.split('\n')  # split by new line

    # results
    results = []
    for idx in range(len(tests)):
        res = compute_prob(tests[idx], dicts)
        results.append(res[0])

    # write language for text
    with open('LangId.result', 'w') as f:
        f.writelines('\n'.join(results))

    # compare solutions and print accuracy
    with open("LangId.sol", 'r') as f:
        solutions = f.read()
        solutions = solutions.split('\n')
        solutions = [item.split(" ")[-1] for item in solutions]

    # wrong lines and their respective numbers
    wrongs = []
    for idx in range(len(solutions)):
        if solutions[idx] == results[idx]:
            continue
        else:
            wrongs.append(idx)

    print("Accuracy is {}".format(1 - (len(wrongs) / len(solutions))))
    print("Incorrectly classified lines are: {}".format(wrongs))


if __name__ == '__main__':
    main()
