import requests
import google.generativeai as genai
from datasets import load_dataset
import time

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyApdIIDxko0YfMZ_xMatRdFSfXN2eaY8WI")

# Unsplash API credentials
UNSPLASH_ACCESS_KEY = "YOUR_UNSPLASH_ACCESS_KEY"

# Set up the model
generation_config = {
    "temperature": 1,
    "top_p": 0.95,
    "top_k": 0,
    "max_output_tokens": 8192,
}

safety_settings = [
    {
        "category": "HARM_CATEGORY_HARASSMENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_HATE_SPEECH",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
    {
        "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
        "threshold": "BLOCK_MEDIUM_AND_ABOVE"
    },
]

model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest",
                              generation_config=generation_config,
                              safety_settings=safety_settings)

# Load car reviews dataset
car_reviews_dataset = load_dataset("florentgbelidji/car-reviews")
user_input = input("")  # Prompt the user to write something
convo = model.start_chat(history=[])


# Function to interact with the chatbot
def chatbot_interaction(user_input):
    if "car review" in user_input.lower():
        return None
    else:
        convo = model.start_chat(history=[])
        convo.send_message(user_input)
        return convo.last.text


# Main function
def main():
    print('-' * 60)
    print("Welcome to the Toyota Review AI Generator!")
    time.sleep(1)
    print("We will help you find reviews for your favorite Toyota!")
    time.sleep(1)
    print('Type "!find" to start your search!')
    time.sleep(1)
    print('Type "!help" for more information!')
    time.sleep(1)
    print('-' * 60)
    while True:
        user_input = input("[USER]: ")
        if "!find" in user_input.lower():
            model = input("Please specify the car model: ").capitalize()
            year = input("Please specify the car year: ").capitalize()
            word = input("What is that one word that you are looking for in a car? ")
            car_review = get_car_review(year, word)
            if car_review[0]:
                print(f"You described a {year} Toyota as: {word}")
                time.sleep(1)
                print(f"The total number of car reviews that matched your query was: {car_review[1]}\n")
                time.sleep(1)
                print("---------- We selected a random car review for you! ----------")
                time.sleep(1)
                print(car_review[0])
            else:
                print("Car review was not found...")
        elif "!help" in user_input.lower():
            print("You have reached the help desk!")
        else:
            chatbot_response = chatbot_interaction(user_input)
            if chatbot_response:
                print("[AI ASSISTANT]: ", chatbot_response)


def get_car_review(year, word):
    car_review = car_reviews_dataset["train"].filter(lambda example: 'Toyota' in example["Vehicle_Title"] and year in example["Vehicle_Title"] and (word in example["Review"] or word.capitalize() in example["Review"]))
    num_car_reviews = len(car_review)
    if len(car_review) > 0:
        return [car_review[0]["Review"], num_car_reviews]
    else:
        return [None, 0]



if __name__ == "__main__":
    main()
