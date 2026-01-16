from datasets import load_dataset
import os
import json

# Load the dataset from Hugging Face
dataset = load_dataset("Amod/mental_health_counseling_conversations")

# Create target folder
target_dir = os.path.join("data", "mental_health_counseling_conversations")
os.makedirs(target_dir, exist_ok=True)

# Save train split as JSON
train_data = dataset["train"]
train_path = os.path.join(target_dir, "combined_dataset.json")

with open(train_path, "w", encoding="utf-8") as f:
    json.dump(train_data.to_dict(), f, ensure_ascii=False, indent=2)

# Optionally save metadata
meta_path = os.path.join(target_dir, "dataset_dict.json")
with open(meta_path, "w", encoding="utf-8") as f:
    json.dump(dataset.info.to_dict(), f, ensure_ascii=False, indent=2)

print(f"Dataset saved to {target_dir}")