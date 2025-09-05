####
#  This is a basic example of how to have an LLM use a tool.
#
# based on https://github.com/daveebbelaar/ai-cookbook/blob/main/patterns/workflows/1-introduction/2-structured.py
#
####


import json
import sys

import requests

from common.watson import load_chat_model

model = load_chat_model()
params = model.params # see if I really need this



def get_weather(latitude, longitude):
    """This is a publicly available API that returns the weather for a given location."""
    response = requests.get(
        f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    )
    data = response.json()
    return data["current"]

def call_function(name, args):
    if name == "get_weather":
        return get_weather(**args)


tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "This tool return the weather for the specified location. The temperature is in celsius and wind speed is in kilometers per hour.",
            "parameters": {
                "type": "object",
                "properties": {
                    "latitude": {"type": "number"},
                    "longitude": {"type": "number"},
                },
                "required": ["latitude", "longitude"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }
]

system_prompt = "You are a helpful weather assistant with access to specialized tools."



def main():
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": "What's the temperature in Berlin today?  I don't need the wind speed."},
    ]

    print("[user] -> ",messages[1]['content'])


    output = model.chat(
        messages=messages,
        tools=tools,
        tool_choice_option="auto",
    )

    response = output['choices'][0]['message']

    #print(response)
    tool_calls = response.get('tool_calls')
    if tool_calls is None:
        print("Unexpected result, please try again")
        return

    for tc in tool_calls:
        # add the response so that the LLM "links" the need to call the tool to the response
        messages.append(response)
        name = tc['function']['name']
        args = json.loads(tc['function']['arguments'])
        result = call_function(name, args)
        # append the result
        messages.append(
            {"role": "tool", "name":name,"tool_call_id": tc['id'], "content": json.dumps(result)}
        )


    #right now, getting an issue where the model "thinks" it needs to run the call again
    output = model.chat(
        messages=messages,
        tools=tools,
        tool_choice_option="auto",
    )

    print("[agent] -> ",output['choices'][0]['message']['content'])




if __name__ == "__main__":
    main()