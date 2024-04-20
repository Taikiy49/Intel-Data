from datasets import load_dataset
from transformers import pipeline
import torch

class ProcessData:
    def processed_data(self):
        dataset = load_dataset("florentgbelidji/car-reviews", split='train')

    def format_dataset(self, sample):
        instruction = f"### Instruction\n{sample['instruction']}"
        context = f"### Context\n{sample['context']}" if len(sample["context"]) > 0 else None
        response = f"### Answer\n{sample['response']}"
        prompt = "\n\n".join([i for i in [instruction, context, response] if i is not None])
        sample["text"] = f"{prompt}{tokenizer.eos_token}"

    def tokenize_function(examples):
        return tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

if __name__ == "__main__":
    processed_data()
    dataset = dataset.map(format_dataset)
    tokenized_dataset = dataset.map(tokenize_function, batched=True, remove_columns=dataset.column_names)
    # Split the dataset into train and test subsets
    train_test_split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
    train_dataset = train_test_split["train"]
    test_dataset = train_test_split["test"]

