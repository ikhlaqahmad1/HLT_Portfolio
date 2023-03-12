import math
import os
import urllib
import nltk
import requests
from urllib import request
from bs4 import BeautifulSoup
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
import string
import pickle

# Stop words in english
stop_words = set(stopwords.words("english"))

"""
    Web crawler function:
        :parameter: URL (Precise preferred)
        
        # This function takes a URL and checks for the response code
        # If response code is invalid, raises an exception
        # Uses beautiful soup to parse html
        # Gets first 25 relevant links
        # Writes all the links to urls.txt file in the home directory
        
"""


# Web crawler function
def web_crawler(starter_url):

    # Starter URL
    response = "null"

    # Check URL for the response code
    try:
        response = requests.get(starter_url)
        response.raise_for_status()
    except requests.HTTPError as exception:
        print(exception)

    # URL data as text
    data = response.text

    # Beautiful Soup html parser
    soup = BeautifulSoup(data, features="html.parser")

    # write urls to a file

    # counter
    counter = 0

    # urls.txt file
    with open('urls.txt', 'w') as f:

        # gets all 'a' attributes
        for link in soup.find_all('a'):
            link_str = str(link.get('href'))
            print(link_str)

            # checks if 'quantum' is present in the query
            if 'quantum' in link_str or 'Quantum' in link_str:

                # if query starts with url
                if link_str.startswith('/url?q='):
                    link_str = link_str[7:]
                    print('MOD:', link_str)

                # if '&' in the link
                if '&' in link_str:
                    i = link_str.find('&')
                    link_str = link_str[:i]

                # if query starts with http and does not have 'google'
                if link_str.startswith('http') and 'google' not in link_str:
                    f.write(link_str + '\n')

                    # Up to 25 valid links
                    if counter > 24:
                        break
                    counter += 1
    # file close urls.txt
    f.close()

    print("end of crawler\n")


"""
    Web Scraper function:
        :parameter: none
        
        # This function has a hdr to facilitate user dependencies
        # It opens and reads all the URLs from urls.txt and prints their title
        # It opens all the URLs from the file
        # Writes all the paragraph, p attributes to the Infiles
        
"""


# web scraper function
def web_scraper():

    # Headers to avoid blockage and facilitate dependencies
    hdr = {
        'user-agent':       ' Mozilla/5.0 (X11; Linux x86_64)'
                            ' AppleWebKit/537.36 (KHTML, like Gecko)'
                            ' Chrome/67.0.3396.99 Safari/537.36',
        'Accept':           'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset':   'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding':  'none',
        'Accept-Language':  'en-US,en;q=0.8',
        'Connection':       'keep-alive'
    }

    # list of links from urls
    list_of_links = []

    # opens urls.txt
    with open('urls.txt', 'r') as f:
        for link in f:

            # list of links from the file
            list_of_links.append(link)

            # opening the url for
            requested_url = urllib.request.Request(url=link, headers=hdr)

            # Reads the URL in decode (utf8)
            html = urllib.request.urlopen(requested_url).read().decode('utf8')

            # parsing the html file
            soup = BeautifulSoup(html, features="html.parser")

            # assigns file name based on the website title
            page_title = soup.title.get_text()

            # prints page title
            print(page_title)

            # Input files from the web scrap
            with open('Raw Text/Infiles/{}.txt'.format(page_title), 'w') as Input_files:
                for raw_data in soup.find_all("p"):
                    Input_files.write(raw_data.get_text())

            # Output files after cleaning
            with open('Raw Text/Outfiles/{}.txt'.format(page_title), 'w') as Output_files:
                for raw_data in soup.find_all("p"):
                    Output_files.write(clean_txt_files(raw_data.get_text()))

    # close file
    f.close()


"""
    Clean raw text function:
        :parameter: string
        :returns: string
        
        # This function takes raw text
        # It lower cases every text
        # Makes sentence tokens and joins it back
        
"""


# Clean txt and sentence tokenize
def clean_txt_files(raw_txt):
    clean_text = raw_txt.lower()
    clean_text = sent_tokenize(clean_text)
    clean_text = " ".join(clean_text)
    return clean_text


"""
    Important terms function:
        :parameter: string, int
        :returns: list
        
        # This function takes string and int
        # Lower cases the string
        # Removes punctuations
        # Tokenizes as words
        # removes stop words in english
        # Calculate inverse document frequency and term frequency
        # Computes their scores and returns the words as a list
"""


# Important terms function
def important_terms(text, num_terms):

    # Convert text to lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Tokenize the text into words
    words = word_tokenize(text)

    # Remove stop words
    words = [word for word in words if word not in stop_words]

    # Calculate term frequencies
    tf = {}
    for word in words:
        tf[word] = tf.get(word, 0) + 1

    # Calculate inverse document frequency
    idf = {}
    for word in tf.keys():
        idf[word] = math.log(len(words) / (sum([1 for doc in words if word in doc]) + 1))

    # Calculate TF-IDF scores
    tfidf = {}
    for word in tf.keys():
        tfidf[word] = tf[word] * idf[word]

    # Sort features by TF-IDF value
    sorted_items = sorted(tfidf.items(), key=lambda x: x[1], reverse=True)

    # Get the most important terms
    terms = [(item[0], round(item[1], 2)) for item in sorted_items[:num_terms]]

    return terms


"""
    Knowledge base function
        :parameter: string
        :returns: dictionary
        
        # It has a list of 10 hard coded select words according to the topic
        # It makes a dictionary of these words as keys with multiple values
        # returns a dictionary of 
        
"""


# knowledge base function
def knowledge_base(file_data):

    # dictionary
    matching_sentences = {}

    # list of 10 important words
    top_terms = ["qubits",
                 "processors",
                 "computing",
                 "algorithm",
                 "simulation",
                 "silicon",
                 "engineering",
                 "vector",
                 "transistors",
                 "temperature"]

    # tokenizes as sentences
    sentences = nltk.sent_tokenize(file_data)

    # checks for the stop words
    sentences = [word for word in sentences if not word in stop_words]

    # checks if the word in the list matches with any sentences
    for sentence in sentences:
        for term in top_terms:
            if term in sentence:
                if term not in matching_sentences.keys():
                    matching_sentences[term] = [sentence]
                else:
                    matching_sentences[term].append(sentence)

    return matching_sentences


# Main()
def main():

    # Web crawler function
    web_crawler("https://en.wikipedia.org/wiki/Quantum_computing")

    # Web scraper
    web_scraper()

    # Path to output files
    path = "./Raw Text/Outfiles"

    # change directory to path
    os.chdir(path)

    file_data = ""

    # iterates over all .txt files in the path directory
    for file in os.listdir():
        if file.endswith(".txt"):
            with open(file, 'r') as f:
                file_data += f.read()

    # gets 40 keywords
    keywords = important_terms(file_data, 40)
    words_dict = knowledge_base(file_data)

    # print all keywords
    print(keywords)

    # words dictionary
    print(words_dict)

    # dump the dictionary as a pickle file in Outfiles
    with open('my_dict.pickle', 'wb') as f:
        pickle.dump(words_dict, f)


if __name__ == "__main__":
    main()
