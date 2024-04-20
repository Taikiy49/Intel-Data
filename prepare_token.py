import os
import json

# FREE access token for usage at: tinyurl.com/pg-intel-hack
import predictionguard as pg
from getpass import getpass


## our access token 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E'
pg_access_token = getpass('Enter your Prediction Guard access token: ')
os.environ['PREDICTIONGUARD_TOKEN'] = pg_access_token


messages = [
{
"role": "system",
"content": """You are a Question answer bot and will give an Answer based on the question you get.
It is critical to limit your answers to the question and dont print anything else.
If you cannot answer the question, respond with 'Sorry, I dont know.'"""
},
{
"role": "user",
"content": "I am going to meet my friend for a night out on the town."
}
]

result = pg.Chat.create(
    model="Neural-Chat-7B",
    messages=messages
)

print(result['choices'][0]['message']['content'].split('\n')[0])