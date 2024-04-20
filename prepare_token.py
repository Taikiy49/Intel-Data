import os
from getpass import getpass
import predictionguard as pg

# FREE access token for usage at: tinyurl.com/pg-intel-hack

pg_access_token = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E' # Enter your Prediction Guard access token here
os.environ['PREDICTIONGUARD_TOKEN'] = pg_access_token

examples = """Neutral: "I'm looking for directions to the nearest bank, can you help me?"
Yoda: "Directions to the nearest bank, you seek. Help you, I can."

Neutral: "It's a pleasure to meet you. What's your name?"
Yoda: "A pleasure to meet you, it is. Yoda, my name is."

Neutral: "I've lost my way, could you point me in the right direction?"
Yoda: "Lost your way, you have. Point you in the right direction, I will."

Neutral: "This weather is wonderful, isn't it?"
Yoda: "Wonderful, this weather is. Agree, do you not?"

Neutral: "I'm feeling a bit under the weather today."
Yoda: "Under the weather, you are feeling today. Better soon, you will be."

Neutral: "Could you please lower the volume? It's quite loud."
Yoda: "Lower the volume, could you please? Quite loud, it is."

Neutral: "I'm here to collect the documents you mentioned."
Yoda: "The documents I mentioned, collect them, you are here to."

Neutral: "Thank you for your assistance. I really appreciate it."
Yoda: "For your assistance, thank you. Appreciate it, I really do."

Neutral: "I'm sorry, I didn't catch your last sentence."
Yoda: "Sorry, I am. Your last sentence, catch it, I did not."

Neutral: "Let's schedule a meeting for next week to discuss the project."
Yoda: "A meeting for next week, schedule, let us. The project, discuss, we will."""

messages = [
{
"role": "system",
"content": "You are a text editor that takes in Neutral text from the user and outputs modified text in the way Yoda would speak similar to these examples:\n\n" + examples
},
{
"role": "user",
"content": 'Neutral: "I am going to meet my friend for a night out on the town."\nYoda:'
}
]

for model in ["Neural-Chat-7B","Hermes-2-Pro-Mistral-7B", "Yi-34B-Chat"]:
    result = pg.Chat.create(
        model,
        messages=messages
    )
    print("="*71)
    print(f"Using Model: {model}")
    print(f"Neutral Text: I am going to meet my friend for a night out on the town.")
    lines = result['choices'][0]['message']['content'].split('\n')
    print(f"How would Yoda say this?: {lines[0]}")
    print("="*71)