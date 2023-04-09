import random


responses = {
    "hi": ["Hello!", "Hi there!", "Hey!"],
    "how are you": ["I'm doing well, thanks for asking!", "I'm fine, how about you?"],
    "bye": ["Goodbye!", "See you later!", "Take care!"]
}


def respond(messages):
    if messages.lower() in responses:
        return random.choice(responses[messages.lower()])
    else:
        return "I'm sorry, I didn't understand what you said."


while True:
    message = input("You: ")
    print("Bot: " + respond(message))


#def main():
    print("Hello")



#if __name__ == "__main__":
 #   main()