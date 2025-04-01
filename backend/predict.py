# # predict.py
# import torch
# from transformers import AutoModelForSequenceClassification, AutoTokenizer
# from preprocessing import preprocess_text  # Import from preprocessing.py

# # Load the trained model and tokenizer
# model = AutoModelForSequenceClassification.from_pretrained("models/arabert_fake_news")
# tokenizer = AutoTokenizer.from_pretrained("models/arabert_fake_news")

# def predict_fake_news(text):
#     """Predict if the text is fake news."""
#     cleaned_text = preprocess_text(text)
#     inputs = tokenizer(cleaned_text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
#     with torch.no_grad():  # Disable gradient calculation for inference
#         outputs = model(**inputs)
#     prediction = torch.argmax(outputs.logits, dim=1).item()
#     labels = {0: "Reliable", 1: "Doubtful", 2: "Fake"}
#     return labels[prediction]

# def verify_source(text):
#     """Verify the source of the text (placeholder logic)."""
#     reliable_sources = ["aljazeera.net", "bbc.com/arabic"]
#     for source in reliable_sources:
#         if source in text.lower():
#             return "Likely reliable source"
#     return "Source not verified"

import json
import os
import stanza
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from joblib import dump, load

# Define paths for pre-saved resources (relative to backend/)
STANZA_MODEL_DIR = "../stanza_resources"
STANZA_PIPELINE_PATH = "../stanza_pipeline.joblib"
TFIDF_VECTORIZER_PATH = "../tfidf_vectorizer.joblib"
TFIDF_MATRIX_PATH = "../tfidf_matrix.joblib"
NEWS_DATA_PATH = "../arabic_news.json"

# Load Stanza pipeline (only if not already saved)
if not os.path.exists(STANZA_MODEL_DIR):
    print("Downloading Stanza Arabic models... (this only happens once)")
    stanza.download('ar', dir=STANZA_MODEL_DIR)
if os.path.exists(STANZA_PIPELINE_PATH):
    print("Loading existing Stanza pipeline...")
    nlp = load(STANZA_PIPELINE_PATH)
else:
    print("Creating new Stanza pipeline and saving it...")
    nlp = stanza.Pipeline(lang='ar', processors='tokenize', dir=STANZA_MODEL_DIR)
    dump(nlp, STANZA_PIPELINE_PATH)

# Load news dataset
if os.path.exists(NEWS_DATA_PATH):
    with open(NEWS_DATA_PATH, 'r', encoding='utf-8') as f:
        news_data = json.load(f)
else:
    raise FileNotFoundError("arabic_news.json not found. Please ensure it exists in the project root.")

# Load TF-IDF resources (vectorizer and matrix)
if os.path.exists(TFIDF_VECTORIZER_PATH) and os.path.exists(TFIDF_MATRIX_PATH):
    print("Loading existing TF-IDF vectorizer and matrix...")
    vectorizer = load(TFIDF_VECTORIZER_PATH)
    tfidf_matrix = load(TFIDF_MATRIX_PATH)
else:
    print("Creating new TF-IDF vectorizer/matrix and saving them...")
    def preprocess_arabic(text):
        doc = nlp(text)
        tokens = [word.text for sentence in doc.sentences for word in sentence.words]
        return ' '.join(tokens)

    vectorizer = TfidfVectorizer(preprocessor=preprocess_arabic)
    corpus_text = [article['content'] for article in news_data]
    tfidf_matrix = vectorizer.fit_transform(corpus_text)
    dump(vectorizer, TFIDF_VECTORIZER_PATH)
    dump(tfidf_matrix, TFIDF_MATRIX_PATH)

# Define preprocessing function
def preprocess_arabic(text):
    doc = nlp(text)
    tokens = [word.text for sentence in doc.sentences for word in sentence.words]
    return ' '.join(tokens)

def predict_fake_news(text, threshold=0.7, top_n=5):
    """
    Predict if the input text is fake news based on similarity to the dataset.
    Returns a string: "likely true" or "likely false or unverified".
    """
    try:
        user_input_vector = vectorizer.transform([preprocess_arabic(text)])
        similarities = cosine_similarity(user_input_vector, tfidf_matrix).flatten()
        top_indices = np.argsort(similarities)[-top_n:][::-1]
        top_similarities = similarities[top_indices]

        prediction = "likely true" if top_similarities[0] >= threshold else "likely false or unverified"
        return prediction  # Return string as expected by app.py
    except Exception as e:
        print(f"Error in predict_fake_news: {e}")
        return "error"

def verify_source(text):
    """
    Verify if a source mentioned in the text exists in the dataset.
    Returns a tuple: (bool, str) - (verified status, content or message).
    """
    try:
        # Basic implementation: check if any source URL is in the text
        for article in news_data:
            if article['source'] in text:
                return True, article['content']
        return False, "Source not found in dataset"
    except Exception as e:
        print(f"Error in verify_source: {e}")
        return False, "Error during source verification"