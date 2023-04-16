"""
    # Ikhlaq Ahmad & Aloksai Choudari
    # ixa190000 & axc190063
    # Dr. Mazidi
    # CS 4395
"""
"""
    # This is the training file for the model.
    # The Training.json file is used to train the model.
    # NLP techniques: TF-IDF & Cosine Similarities
    
    Methods:
        preprocess(): text
        :return: text
"""
# Train.py train the model based on the intents file
import json
import string
from scipy.sparse import save_npz, csr_matrix
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.stem import PorterStemmer

# stop words
stop_words = set(stopwords.words('english'))
stemmer = PorterStemmer()

training_file = "Training.json"

# Load JSON data
with open(training_file, 'r') as f:
    data = json.load(f)

# Extract questions and answers from JSON data
patterns = [d["patterns"] for d in data]
responses = [d["responses"] for d in data]


# Preprocess text data
def preprocess(text):
    # Tokenize text
    tokens = word_tokenize(text)
    # Remove stop words and punctuation
    tokens = [stemmer.stem(token.lower()) for token in tokens if token not in stop_words and token not in string.punctuation]
    # Join tokens back into a string
    preprocessed_text = ' '.join(tokens)
    return preprocessed_text


preprocessed_patterns = [preprocess(str(pattern)) for pattern in patterns]
preprocessed_responses = [preprocess(str(response)) for response in responses]


# Convert preprocessed text data into numerical representation using TF-IDF
tfidf_vectorizer = TfidfVectorizer()
tfidf_questions = tfidf_vectorizer.fit_transform(preprocessed_patterns)
tfidf_answers = tfidf_vectorizer.transform(preprocessed_responses)

# Train machine learning model on numerical data
cosine_similarities = cosine_similarity(tfidf_questions, tfidf_answers)

# Convert cosine_similarities to a sparse CSR matrix
cosine_similarities_sparse = csr_matrix(cosine_similarities)

# Save cosine_similarities_sparse as a .npz file
save_npz('cosine_similarities.npz', cosine_similarities_sparse)

