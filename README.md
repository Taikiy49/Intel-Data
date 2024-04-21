## LA Hacks 2024
[https://lahacks.com/live/home]

# Overview
This repository contains the Car Reviews Dataset, curated by [florentgbelidji/car-reviews](https://huggingface.co/datasets/florentgbelidji/car-reviews) from Hugging Face. The dataset comprises reviews of various car models along with associated metadata such as review date, author name, vehicle title, review title, review text, and rating. 
In addition to traditional machine learning tasks, the Car Reviews Dataset can be leveraged for advanced natural language processing (NLP) tasks using powerful Large Language Models (LLMs) like LLMA2. These models excel in tasks such as sentiment analysis, text generation, and language understanding. By fine-tuning LLMA2 on the dataset, users can extract deeper insights from the reviews and enhance decision-making processes related to car purchases. The web application is implemented by HTML,CSS, Flask (back-end) and Google Generative AI (Gemini) model for text generation in order to interacts with a dataset for car reviews.

# Dataset 
Contains 37,000 rows of training data.

Columns


Review_Date (string) - Date of the review.

Author_Name (string) - Name of the review author.

Vehicle_Title (string) - Title of the vehicle.

Review_Title (string) - Title of the review.

Review (string) - Text of the review.

Rating (int64) - Rating given by the reviewer.

<img width="1356" alt="Screenshot 2024-04-20 at 4 16 10 PM" src="https://github.com/Taikiy49/Intel-Data/assets/90120932/64df5a2a-1e5e-4b45-82bf-c927b8605f43">

# 🌟 Getting Started with Intel Developer Cloud 🌟
To prototype and build your GenAI solution on Intel Developer Cloud, you'll first need to create a free account. Here's how:

Go to cloud.intel.com/hoohacks and click "Get Started" if you don't have an account yet.

Register for a Standard (free) account by filling out the sign-up form.

Once registered, log in with your new credentials. You'll land on the Intel Developer Cloud Console home page at https://console.cloud.intel.com.

From the home page or the left sidebar, navigate to "Training" and look for the "Gen AI Essentials" content. This is where you'll find hands-on tutorials for building GenAI applications.

If you are developing in PyTorch, select the pytorch-gpu kernel and to use Intel GPUs:

```
import torch

import intel_extension_for_pytorch as ipex

print(f"GPU is: {torch.xpu.get_device_name()}")
```

# Setting up the Environment ⚙️
```
pip install flask ngrok
```

```
!echo "installing required python libraries, please wait..."
!{sys.executable} -m pip install --upgrade predictionguard #> /dev/null # for accessing LLM APIs
!{sys.executable} -m pip install --upgrade  "transformers>=4.38.*" #> /dev/null
!{sys.executable} -m pip install --upgrade  "datasets>=2.18.*" #> /dev/null
!{sys.executable} -m pip install --upgrade "
```

Create a simple Flask server in a new Python file (Default port is 5000):
```
from flask import Flask, request, jsonify
app = Flask(__name__)

@app.route('/api', methods=['POST'])
def api():
    data = request.get_json()
    # Process the request and generate a response
    response = {'message': 'Hello, World!'}
    return jsonify(response)

if __name__ == '__main__':
    app.run()
```
In a new Python file, set up ngrok to expose the Flask server:

```
from pyngrok import ngrok

# Start ngrok tunnel
public_url = ngrok.connect(5000)
print(f'Public URL: {public_url}')
```

```
ngrok http http://127.0.0.1:5000
```


Summarize the reviews by hitting summarize button below:


<img width="1034" alt="summarize_all_reviews" src="https://github.com/Taikiy49/Intel-Data/assets/90120932/933c5b71-e3b0-4dce-8dc7-7659a62d4a0d">





Keep all positive reviews only, for example


<img width="891" alt="positive_reviews" src="https://github.com/Taikiy49/Intel-Data/assets/90120932/f1850ee4-318f-49a2-bcea-de331860364f">





Interact with AI Gemini chatbot


<img width="739" alt="Car_Review" src="https://github.com/Taikiy49/Intel-Data/assets/90120932/10e64c59-1aec-497e-993d-5408b8f76acd">


Domain from ngrok sever: https://2de2-164-67-154-31.ngrok-free.app
# Community
This dataset is intended for various applications such as sentiment analysis, natural language processing, and AI decision-making processes related to car purchases. The dataset can be utilized to train machine learning models for tasks like review sentiment classification, recommendation systems, and more.

For more details and usage examples, refer to the original source.
