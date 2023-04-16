"""
    # Ikhlaq Ahmad
    # ixa190000
    # Dr. Mazidi
    # CS 4395
"""


# Dependencies
import json
import os
import random
import string

import numpy as np
from scipy.sparse import load_npz
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer

# Training module from Train.py
from Homework9.Train import tfidf_questions, tfidf_vectorizer

# User chat history file
user_history_file = "user_history"

# Stopword to remove reduce sentence complexity (English)
stop_words = set(stopwords.words('english'))

# Stemmer module of nltk to remove suffixes/prefixes
stemmer = PorterStemmer()

# Load cosine similarities from the training file
cosine_similarities = load_npz('cosine_similarities.npz')

# Load JSON data
with open('Training.json', 'r') as f:
    data = json.load(f)

# Extract questions from JSON data
questions = [d["patterns"] for d in data]


# Generate Responses using user-related queries
def generate_response(user_input):

    # Preprocess user input
    preprocessed_user_input = ' '.join([stemmer.stem(token.lower()) for token in word_tokenize(user_input)
                                        if token.lower() not in stop_words and token not in string.punctuation])
    # If user(s) request is empty
    if preprocessed_user_input == "":
        return "I'm sorry, I don't understand."
    else:

        # Convert preprocessed user input into numerical representation using TF-IDF
        tfidf_user_input = tfidf_vectorizer.transform([preprocessed_user_input])

        # Calculate cosine similarities between user input and questions in the JSON data
        cosine_similarities_user_input = cosine_similarity(tfidf_user_input, tfidf_questions)

        # Find the index of the question with the highest cosine similarity to the user input
        index_most_similar_question = np.argmax(cosine_similarities_user_input)

        # If relevant response is not found
        if index_most_similar_question == 0:
            return "I'm sorry, I don't know about that. I can only answer questions about computers"
        else:
            # Return the corresponding answer from the JSON data
            size = len(data[index_most_similar_question]['responses'])

            # Randomizes the response
            return str(data[index_most_similar_question]['responses'][random.randint(0, size-1)])


# User authentication
def user_authentication(user_name, password):

    # load the existing data from the JSON file
    with open('Users.json', 'r') as user_file:
        user_data = json.load(user_file)

    # check if the username and password match
    for user_profile in user_data["users"]:
        if user_profile["username"] == user_name and user_profile["password"] == password:
            print("User authenticated!")
            return True

    # New user object
    new_user = {
        "username": user_name,
        "password": password,
    }
    user_data["users"].append(new_user)
    print("New User Created!")

    # Write the updated Users.json back to the JSON file
    with open('Users.json', 'w') as user_file:
        json.dump(user_data, user_file, indent=4)
        user_file.close()


# Save user model
def save_user_model(user_model):
    # Changes the directory to user_history
    directory = user_history_file
    filename = os.path.join(directory, f"{user_model['id']}.json")

    # Dumps all the user record in user_history
    with open(filename, "w") as history:
        json.dump(user_model, history, indent=4)


# get User Model
def get_user_model(user_id):

    # Changes the directory to user_history
    directory = user_history_file
    filename = os.path.join(directory, f"{user_id}.json")

    # Changes the path to file
    if os.path.isfile(filename):
        with open(filename, "r") as history:
            user_model = json.load(history)
    else:
        user_model = {"id": user_id, "name": "", "age": 0, "conversation": []}
        save_user_model(user_model)
    return user_model


# Main
def main():

    # Welcome
    print("Welcome to the Chatbot!")

    # Gets name and password
    name = input("Enter the user name: ")
    password = input("Enter the password: ")

    # Gets the user file (if present) or creates one
    user_model = get_user_model(name)

    # Welcome back
    if user_authentication(name, password):
        print("Welcome Back!, ", name)

    # Exit Conditions
    exit_conditions = (":q", "quit", "exit")

    while True:
        query = input("You: ")

        if query in exit_conditions:
            print("Good Bye!")
            break
        else:

            # Loops until user exits
            bot_response = generate_response(query)
            print("Bot: ", bot_response)

            # Appends User's conversations
            user_model["conversation"].append({"user": True, "message": query})
            save_user_model(user_model)

            # process user message and generate bot response
            user_model["conversation"].append({"user": False, "message": bot_response})
            save_user_model(user_model)


# Main
if __name__ == "__main__":
    main()
