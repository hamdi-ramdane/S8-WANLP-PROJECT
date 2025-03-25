# preprocessing.py
import pandas as pd
import stanza
from transformers import AutoTokenizer

# Initialize Stanza pipeline for Arabic (large model)
stanza.download('ar')  # Download Arabic model
nlp = stanza.Pipeline(lang='ar', processors='tokenize,lemma', use_gpu=False)

# Load AraBERT tokenizer
tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv2")

# Example Arabic stopwords (replace with a comprehensive list if needed)
arabic_stopwords = ["و", "في", "من", "إلى", "على"]

def preprocess_text(text):
    """Clean and preprocess Arabic text using Stanza."""
    # Process text with Stanza
    doc = nlp(text)
    # Tokenize and lemmatize, removing stopwords
    cleaned_tokens = [word.lemma for sent in doc.sentences for word in sent.words if word.text not in arabic_stopwords]
    return " ".join(cleaned_tokens)

def tokenize_text(text, max_length=128):
    """Tokenize text using AraBERT tokenizer."""
    return tokenizer(text, padding="max_length", truncation=True, max_length=max_length, return_tensors="pt")