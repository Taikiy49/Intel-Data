import requests
import google.generativeai as genai
from datasets import load_dataset

# Configure the API key for Google Generative AI
genai.configure(api_key="AIzaSyApdIIDxko0YfMZ_xMatRdFSfXN2eaY8WI")

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

# Function to book a test drive
def book_test_drive(make, model, year, date, time):
    # Your test drive booking API integration here
    return f"Test drive booked for {make} {model} {year} on {date} at {time}."

# Function to find nearby car dealerships
def find_nearby_dealerships(location):
    # Your nearby dealerships API integration here
    return f"Nearest car dealerships to {location} are: Dealership A, Dealership B, Dealership C."

# Function to provide car buying advice
def provide_car_buying_advice(budget):
    # Your car buying advice API integration here
    return "Car buying advice: Consider fuel efficiency, safety features, and resale value when choosing a car within your budget."

# Function to interact with the chatbot
def chatbot_interaction(user_input):
    convo = model.start_chat(history=[])
    convo.send_message(user_input)
    return convo.last.text

# Main function
def main():
    print('-' * 60)
    print("Welcome to Car Assistant")
    print('-' * 60)
    while True:
        user_input = input("[USER] You: ")
        chatbot_response = chatbot_interaction(user_input)
        print("[CAR ASSISTANT] Bot: ", chatbot_response)
        

        if "test drive" in user_input:
            make = input("Please specify the car make: ").capitalize()
            model = input("Please specify the car model: ").capitalize()
            year = input("Please specify the car year: ")
            date = input("Please specify the date (MM/DD/YYYY): ")
            time = input("Please specify the time: ")
            print(book_test_drive(make, model, year, date, time))
        elif "dealership" in user_input:
            location = input("Please specify the location: ")
            print(find_nearby_dealerships(location))
        elif "buying advice" in user_input:
            budget = input("Please specify your budget: ")
            print(provide_car_buying_advice(budget))
        elif "car review" in user_input:
            make = input("Please specify the car make: ").capitalize()
            car_review = get_car_review(make)
            if car_review:
                print(f"Car review for {make}")
                print(car_review)
            else:
                print("Car review not found.")
        elif user_input.lower() == "exit":
            print("Goodbye!")
            break

def get_car_review(make):
    car_review = car_reviews_dataset["train"].filter(lambda example: example["Vehicle_Title"])
    if len(car_review) > 0:
        return car_review[0]["Review"]
    else:
        return None

if __name__ == "__main__":
  main()
