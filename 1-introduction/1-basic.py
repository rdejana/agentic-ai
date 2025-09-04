import json
import os

from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters, TextGenParameters
from ibm_watsonx_ai.foundation_models.schema import TextChatResponseFormat, TextChatResponseFormatType
from ibm_watsonx_ai.foundation_models import ModelInference
from dotenv import load_dotenv

load_dotenv()  #load

project_id = os.getenv("WX_PROJECT_ID")
credentials = Credentials(
    url=os.getenv("WX_URL"),
    api_key=os.getenv("WX_API_KEY"),
)

model_id = "meta-llama/llama-3-2-90b-vision-instruct"

params = TextChatParameters(
    max_tokens=1024,
    temperature=1
)

model = ModelInference(
    model_id=model_id,
    credentials=credentials,
    project_id=project_id,
    params=params
)

output = model.chat(
    messages=[
        {"role": "system", "content": "You're a helpful assistant."},
        {"role": "system", "content": "Return your response as text"} ,
        {
            "role": "user",
            "content": "Write a limerick about the Python programming language.",
        },
    ],
    params=params
)

# now let's get the output
response = output['choices'][0]['message']['content']
#print( output['choices'][0]['message'])
print(response)
