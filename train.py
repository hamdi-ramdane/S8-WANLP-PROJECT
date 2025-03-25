import pandas as pd
import torch
from sklearn.model_selection import train_test_split
from torch.utils.data import Dataset, DataLoader
from transformers import AutoModelForSequenceClassification, Trainer, TrainingArguments, AutoTokenizer
from preprocessing import preprocess_text  # Import from preprocessing.py

# Load and preprocess data
csv_file = "data/arabic_news.csv"  # Adjust path if needed
df = pd.read_csv(csv_file)

# Debug: Check CSV structure
print("CSV shape:", df.shape)
print("Columns:", df.columns.tolist())

# Use the first column dynamically (assuming it’s the text column)
text_column = df.columns[0]  # Replace 'text' with actual column name
df['cleaned_text'] = df[text_column].apply(preprocess_text)

# Ensure no missing data
df = df.dropna(subset=['cleaned_text', 'label'])
print("After dropna, shape:", df.shape)

# Split data into train and test sets (before tokenizing)
texts = df['cleaned_text'].tolist()
labels = df['label'].tolist()
train_texts, test_texts, train_labels, test_labels = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

# Debug: Verify lengths
print("Train texts:", len(train_texts), "Train labels:", len(train_labels))
print("Test texts:", len(test_texts), "Test labels:", len(test_labels))

# Tokenize after splitting
tokenizer = AutoTokenizer.from_pretrained("aubmindlab/bert-base-arabertv2")
train_encodings = tokenizer(train_texts, truncation=True, padding=True, max_length=128, return_tensors="pt")
test_encodings = tokenizer(test_texts, truncation=True, padding=True, max_length=128, return_tensors="pt")

# Custom Dataset class
class ArabicNewsDataset(Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: val[idx].clone().detach() for key, val in self.encodings.items()}  # Extract single sample
        item['labels'] = torch.tensor(self.labels[idx], dtype=torch.long)
        return item

    def __len__(self):
        return len(self.labels)

# Create datasets
train_dataset = ArabicNewsDataset(train_encodings, train_labels)
test_dataset = ArabicNewsDataset(test_encodings, test_labels)

# Load pre-trained AraBERT model
model = AutoModelForSequenceClassification.from_pretrained("aubmindlab/bert-base-arabertv2", num_labels=3)

# Define training arguments
training_args = TrainingArguments(
    output_dir="./models/arabert_fake_news",
    num_train_epochs=3,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    warmup_steps=500,
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=10,
    # evaluation_strategy="epoch", # old version 
    eval_strategy="epoch",
    save_strategy="epoch",
    load_best_model_at_end=True,
)

# Initialize Trainer
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=train_dataset,
    eval_dataset=test_dataset,
)

# Train the model
trainer.train()

# Save the model and tokenizer
model.save_pretrained("models/arabert_fake_news")
tokenizer.save_pretrained("models/arabert_fake_news")

print("Training complete. Model saved to 'models/arabert_fake_news'.")