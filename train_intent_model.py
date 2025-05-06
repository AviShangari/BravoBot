import pandas as pd
import torch
from torch.utils.data import Dataset, DataLoader
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification, Trainer, TrainingArguments
from sklearn.preprocessing import LabelEncoder
import os

# Load data
df = pd.read_csv("intent_data.csv")

# Encode labels
label_encoder = LabelEncoder()
df["label"] = label_encoder.fit_transform(df["intent"])
labels = df["label"].tolist()
intents = df["intent"].tolist()
texts = df["text"].tolist()

# Save label mapping
os.makedirs("intent_model", exist_ok=True)
with open("intent_model/labels.txt", "w") as f:
    for i, label in enumerate(label_encoder.classes_):
        f.write(f"{i},{label}\n")

# Dataset class
class IntentDataset(Dataset):
    def __init__(self, texts, labels, tokenizer):
        self.encodings = tokenizer(texts, truncation=True, padding=True)
        self.labels = labels

    def __len__(self):
        return len(self.labels)

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        item["labels"] = torch.tensor(self.labels[idx])
        return item

# Tokenizer and model
tokenizer = DistilBertTokenizerFast.from_pretrained("distilbert-base-uncased")
model = DistilBertForSequenceClassification.from_pretrained("distilbert-base-uncased", num_labels=len(label_encoder.classes_))

# Dataset and loader
dataset = IntentDataset(texts, labels, tokenizer)

# Training setup
training_args = TrainingArguments(
    output_dir="intent_model",
    num_train_epochs=5,
    per_device_train_batch_size=8,
    logging_dir="intent_model/logs",
    logging_steps=5,
    save_strategy="epoch",
    # evaluation_strategy="no"
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)

# Train
trainer.train()
trainer.save_model("intent_model")
tokenizer.save_pretrained("intent_model")
