import torch
from transformers import DistilBertTokenizerFast, DistilBertForSequenceClassification
import os

class IntentClassifier:
    def __init__(self, model_path="intent_model"):
        self.tokenizer = DistilBertTokenizerFast.from_pretrained(model_path)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
        self.model.eval()

        # Load label mapping
        self.label_map = {}
        with open(os.path.join(model_path, "labels.txt"), "r") as f:
            for line in f:
                idx, label = line.strip().split(",")
                self.label_map[int(idx)] = label

    def predict_intent(self, text):
        inputs = self.tokenizer(text, return_tensors="pt", truncation=True, padding=True)
        with torch.no_grad():
            outputs = self.model(**inputs)
            probs = torch.nn.functional.softmax(outputs.logits, dim=1)
            pred_label = torch.argmax(probs, dim=1).item()
            return self.label_map[pred_label]
