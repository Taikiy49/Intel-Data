from datasets import load_dataset
from transformers import AutoTokenizer

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
        sample["text"] = f"{prompt}{self.tokenizer.eos_token}"
        return sample

    def tokenize_function(self, examples):
        return self.tokenizer(examples["text"], padding="max_length", truncation=True, max_length=512)

    def run(self):
        vehicle_list = []
        self._dataset = self._dataset.map(self.format_dataset)
        # for i in range(self._dataset.num_rows):
        for i in range(3):
            info_dict = {}
            info_dict['role'] = self._dataset["Vehicle_Title"][i]
            info_dict['content'] = self._dataset["Review"][i]
            vehicle_list.append(info_dict)
        return vehicle_list



