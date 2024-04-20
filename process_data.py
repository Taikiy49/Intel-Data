from datasets import load_dataset

def processed_data():
    dataset = load_dataset('https://huggingface.co/datasets/florentgbelidji/car-reviews')
    return dataset

if __name__ == "__main__":
    processed_data()

