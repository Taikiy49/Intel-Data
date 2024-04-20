import os
import predictionguard as pg
from process_data import ProcessData

class ChatData:
    def __init__(self, data):
        self._pg_access_token = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E'
        self._data_set = data  # data will be imported from another file later

    def _create_connection(self):
        os.environ['PREDICTIONGUARD_TOKEN'] = self._pg_access_token

    def run(self):
        result = pg.Chat.create(
            model="Neural-Chat-7B",
            messages=self._data_set
        )

        print(result['choices'][0]['message']['content'].split('\n')[0])
    

if __name__ == "__main__":
    process_data = ProcessData()
    process_data.processed_data()
    # lets see if this works...
    data_list = process_data.run()
    chat_data = ChatData(data_list)
    chat_data._create_connection()
    chat_data.run()
