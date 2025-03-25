# predict.py
import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
from preprocessing import preprocess_text  # Import from preprocessing.py

# Load the trained model and tokenizer
model = AutoModelForSequenceClassification.from_pretrained("models/arabert_fake_news")
tokenizer = AutoTokenizer.from_pretrained("models/arabert_fake_news")

def predict_fake_news(text):
    """Predict if the text is fake news."""
    cleaned_text = preprocess_text(text)
    inputs = tokenizer(cleaned_text, padding="max_length", truncation=True, max_length=128, return_tensors="pt")
    with torch.no_grad():  # Disable gradient calculation for inference
        outputs = model(**inputs)
    prediction = torch.argmax(outputs.logits, dim=1).item()
    labels = {0: "Reliable", 1: "Doubtful", 2: "Fake"}
    return labels[prediction]

def verify_source(text):
    """Verify the source of the text (placeholder logic)."""
    reliable_sources = ["aljazeera.net", "bbc.com/arabic"]
    for source in reliable_sources:
        if source in text.lower():
            return "Likely reliable source"
    return "Source not verified"