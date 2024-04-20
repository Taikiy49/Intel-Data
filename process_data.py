from datasets import load_dataset
from transformers import pipeline, AutoTokenizer
import torch

class ProcessData:
    def __init__(self):
        self._dataset = None
        self.tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")

    def processed_data(self):
        self._dataset = load_dataset("florentgbelidji/car-reviews", split='train')

    def format_dataset(self, sample):
        vehicle_title = f"### Vehicle Title\n{sample['Vehicle_Title']}"
        review = f"### Review\n{sample['Review']}" 
        rating = f"### Rating\n{sample['Rating']}"
        prompt = "\n\n".join([i for i in [vehicle_title, review, rating] if i is not None])
        sample["Author_Name"] = f"{prompt}{self.tokenizer.eos_token}"

    def tokenize_function(self, examples):
        return self.tokenizer(examples["Vehicle_Title"], padding="max_length", truncation=True, max_length=512)

    def run(self):
        self._dataset = self._dataset.map(self.format_dataset)
        tokenized_dataset = self._dataset.map(self.tokenize_function, batched=True, remove_columns=self._dataset.column_names)
        # Split the dataset into train and test subsets
        train_test_split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
        train_dataset = train_test_split["train"]
        test_dataset = train_test_split["test"]
        print(train_dataset)
        print(test_dataset)

if __name__ == "__main__":
    process_data = ProcessData()
    process_data.processed_data()
    process_data.run()
