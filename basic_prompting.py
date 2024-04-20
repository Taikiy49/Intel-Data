import os
import predictionguard as pg

os.environ['PREDICTIONGUARD_TOKEN'] = '239cb013fbc54bd2b82de8433ff8eb4b'

response = pg.Completion.create(model="Neural-Chat-78", prompt="The best joke I know is: ")
print(response['choices'][0]['text'])


# this is where I will use my generated API key!

