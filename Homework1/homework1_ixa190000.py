# Homework 1
# HLT CS 4395
# Ikhlaq Ahmad
# ixa190000

# Dependencies
import pickle
import sys
import re


# Person Class
# This class has two methods: init(), display()

class Person:

    # init() takes two params: self, string
    def __init__(self, data):
        parsed_data = process_text(data)
        self.last_name = parsed_data[0]
        self.first_name = parsed_data[1]
        self.middle_initial = parsed_data[2]
        self.id = parsed_data[3]
        self.phone = parsed_data[4]

    # display() prints all attributes of init()
    def display(self):
        print(self.last_name, self.first_name, self.middle_initial, self.id, self.phone)
        return self.first_name, self.middle_initial, self.last_name, self.id, self.phone


# Processes_text() takes one params: string
def process_text(inputs):

    # Splits string with delimiter ','
    tokens = inputs.strip().split(',')

    # Changes name to UPPER CASE and Middle initial to 'X', if not applicable
    for idx in range(len(tokens[:3])):
        if tokens[idx]:
            tokens[idx] = tokens[idx].lower()
            tokens[idx] = tokens[idx][0].upper() + tokens[idx][1:]
        else:
            tokens[idx] = 'X'

    # ID pattern: 2 letter + 4 digits
    id_pattern = "^[A-Za-z]{2}[0-9]{4}$"

    # using regular expression (re), keeps asking user for correct input
    while not re.match(id_pattern, tokens[3]):
        print('ID invalid', tokens[3])
        print('ID is two letters followed by 4 digits. Please enter a valid id:')
        tokens[3] = input()
        tokens[3] = tokens[3].upper()

    # Phone number pattern
    phone_pattern = "^[0-9]{3}-[0-9]{3}-[0-9]{4}$"

    # Corrects phone number pattern
    while not re.match(phone_pattern, tokens[4]):
        print('Phone ', tokens[4], ' is invalid')
        print('Enter phone number in form 123-456-7890: ')
        tokens[4] = input()
    return tokens


# main()
def main(args):
    num_of_args = len(args)

    # System Args Exceptions
    if num_of_args != 1:
        raise Exception("Invalid number of argument(s)!")

    # File name to be processed
    pat = ' '.join(args)

    with open(pat) as csv_file:
        next(csv_file)
        data = csv_file.read().splitlines()

    # person dictionary
    persons = {}

    # Iterates over data line from csv file
    for person in data:
        p = Person(person)
        if not p.id in persons.keys():
            persons[p.id] = p
        else:
            print("Error person {} exists in data file.".format(p.id))

    # pickle dump
    with open('persons', 'wb') as file:
        pickle.dump(persons, file)
        file.close()

    # open and verify file in binary
    with open('persons', 'rb') as file:
        persons = pickle.load(file)
        file.close()

    # loop over to print Person objects
    for p_id, person in persons.items():
        print('\nEmployee id: {}'.format(person.id))
        print('\t', person.first_name, person.middle_initial, person.last_name)
        print('\t', person.phone)


if __name__ == "__main__":

    # System Arg
    main(sys.argv[1:])
