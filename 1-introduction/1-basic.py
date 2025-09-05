import json
import os

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters, TextGenParameters
from ibm_watsonx_ai.foundation_models.schema import TextChatResponseFormat, TextChatResponseFormatType
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv
import common.watson

from common.watson import load_chat_model


model = load_chat_model()
params = model.params # see if I really need this
print(params)

output = model.chat(
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {"role": "system", "content": "Return your response as text"} ,
        {
            "role": "user",
            #orginally a limerick, but how about a sonnet
            "content": "Write a sonnet about the Python programming language.",
        },
    ],
    #params=params
)

# now let's get the output
print(output)
response = output['choices'][0]['message']['content']
print(response)
