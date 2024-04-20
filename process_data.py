from datasets import load_dataset
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch
from peft import get_peft_model, LoraConfig, TaskType
from transformers import DataCollatorForLanguageModeling 
from transformers import Trainer
import os

device = "cpu" #"xpu" if torch.xpu.is_available() else "cpu"
model_name = "microsoft/phi-1_5"
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name).to(device)
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
        self._dataset = self._dataset.map(self.format_dataset)
        tokenized_dataset = self._dataset.map(self.tokenize_function, batched=True, remove_columns=self._dataset.column_names)
        # Split the dataset into train and test subsets
        train_test_split = tokenized_dataset.train_test_split(test_size=0.1, seed=42)
        self._train_dataset = train_test_split["train"]
        self._test_dataset = train_test_split["test"]
        
    def create_model(self):
        config = LoraConfig(
            r=16,
            lora_alpha=2,
            target_modules=["fc1", "fc2","Wqkv", "out_proj"],
            lora_dropout=0.05,
            bias="none",
            task_type="CAUSAL_LM"
        )

        self._model = get_peft_model(model, config)
        self._model.print_trainable_parameters()

    def train(self):
        os.environ["TOKENIZERS_PARALLELISM"] = "0"  # prevent warnings from training on process forking
        trainer = Trainer(
            model=self.model,
            train_dataset=self._train_dataset,
            eval_dataset=self._test_dataset,
            data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False)
        )

        if torch.xpu.is_available():
            torch.xpu.empty_cache()
        results = trainer.train()

        trainer.save_model("./fine_tuned_model")


if __name__ == "__main__":
    process_data = ProcessData()
    process_data.processed_data()
    process_data.run()
    process_data.create_model()
    process_data.train()
