import os
from getpass import getpass
import predictionguard as pg
from process_data import ProcessData

# from sentence_transformers import SentenceTransformer # these we will import later
# import faiss # these we will import later

class ChatData:
    def __init__(self, data):
        self._pg_access_token = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E' 
        self._data_set = data # data will be imported from another file later

    def _create_connection(self):
        os.environ['PREDICTIONGUARD_TOKEN'] = self._pg_access_token

    def run(self):
        # self._data_set will replace messages later!
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

if __name__ == "__main__":
    process_data = ProcessData()
    process_data.processed_data()
    # lets see if this works...
    data_list = process_data.run()
    print(data_list)
    chat_data = ChatData(data_list)
    chat_data._create_connection()
    chat_data.run()
    