import os
import predictionguard as pg
from sentence_transformers import SentenceTransformer
from sklearn.neighbors import NearestNeighbors

class ChatData:
    def __init__(self):
        self._pg_access_token = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E'
        self.model = SentenceTransformer('paraphrase-MiniLM-L6-v2')  # Initialize Sentence Transformer model
        self.index = NearestNeighbors(metric='cosine')  # Initialize Nearest Neighbors index

    def _create_connection(self):
        os.environ['PREDICTIONGUARD_TOKEN'] = self._pg_access_token

    def initialize_index(self, knowledge_base):
        self.index.fit(self.model.encode(knowledge_base))

    def rag_answer(self, question, knowledge_base, prompt_template):
        try:
            question_embedding = self.model.encode([question])

            _, most_relevant_idx = self.index.kneighbors(question_embedding, n_neighbors=1)
            relevant_chunk = knowledge_base[most_relevant_idx[0][0]]
            prompt = prompt_template.format(relevant_chunk, question)

            result = pg.Completion.create(
                model="Neural-Chat-7B", 
                prompt=prompt
            )
            return result['choices'][0]['text']

        except Exception as e:
            print(f"An error occurred: {str(e)}")
            return "Sorry, something went wrong. Please try again later."

    def questions(self):
        knowledge_base = [
            "Prediction Guard uses high-performance servers with state-of-the-art GPUs for its AI services.",
            "Prediction Guard's headquarters is located in San Francisco, California.",
            "Intel Liftoff is a program aimed at boosting AI startups, and Prediction Guard has a partnership with Liftoff."
        ]
        prompt_template = "Knowledge: {}\nQuestion: {}"

        print("="*71)
        for i, question in enumerate([
            "What hardware does Prediction Guard use for its AI services?",
            "Where is Prediction Guard's headquarters located?",
            "What is Intel Liftoff and what is Prediction Guard's relationship to Liftoff?"
        ]):
            response = self.rag_answer(question, knowledge_base, prompt_template)
            print(f"Question {i+1}: {question}")
            print(f"Response {i+1}: {response}")
            print("="*71)

    def run(self):
        messages = [
            {
                "role": "system",
                "content": """You are a Question answering bot and will give an Answer based on the question you get.
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
    chat_data = ChatData()
    chat_data._create_connection()
    chat_data.run()
    chat_data.questions()
