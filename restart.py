import os
import json

# FREE access token for usage at: tinyurl.com/pg-intel-hack
import predictionguard as pg
from getpass import getpass

pg_access_token = 'q1VuOjnffJ3NO2oFN8Q9m8vghYc84ld13jaqdF7E'
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


import predictionguard as pg
from sentence_transformers import SentenceTransformer
import faiss

knowledge_base = [
    "Prediction Guard is an AI company that provides APIs for language models.",
    "Prediction Guard is an Intel Liftoff startup",
    "Intel Liftoff is Intel's premier startup accelerator program for early stage startups",
    "Prediction Guard offers a variety of models for different tasks like text generation, classification, and question answering.",
    "Prediction Guard's APIs are easy to use and integrate into your applications.",
    "Prediction Guard is deployed on the Intel Developer Cloud using Intel Habana Gaudi 2 machines.",
    "Intel Habana Gaudi 2 is a purpose-built AI processor designed for high-performance deep learning training and inference.",
    "Gaudi 2 offers high efficiency, scalability, and ease of use for AI workloads.",
    "By leveraging Gaudi 2 on the Intel Developer Cloud, Prediction Guard can provide powerful and efficient AI capabilities to its users."
]
prompt_template = f"""
### Instruction:
Read the below input context and respond with a short answer to the given question.
Use only the information in the below input to answer the question.
It is critical to limit your answers to the question and dont print anything else.
If you cannot answer the question, respond with "Sorry, I don't know."

### Input:
Context: {{}}
Question: {{}}

### Response:
"""

model = SentenceTransformer("all-MiniLM-L6-v2") # a small and fast embedding model
kb_embeddings = model.encode(knowledge_base)
index = faiss.IndexFlatL2(kb_embeddings.shape[1]) # 384
index.add(kb_embeddings)