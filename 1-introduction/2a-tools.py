##
# Tool example using an LLM with a simple calculator
#
##

# 2 very simple "tools", add and multiple

from common.watson import load_chat_model
import json

#from langchain_ibm.chat_models import convert_to_openai_tool

def add(a: int,b: int):
    # model isn't returning the right types for the args, so forcing to in
    return int(a)+ int(b)

def multiply(a: int,b: int):
    # model isn't returning the right types for the args, so forcing to in
    #print(type(a))
    return int(a) * int(b)



def add_schema():
    schema =  {
        "type": "function",
        "function": {
            "name": "add",
            "description": "This tool adds two integers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": { "description": "An integer value",
                        "type": "integer"},
                    "b": { "description": "An integer value",
                           "type": "integer"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }

    return schema

def multiply_schema():
    schema =  {
        "type": "function",
        "function": {
            "name": "multiply",
            "description": "This tool multiplies two integers together.",
            "parameters": {
                "type": "object",
                "properties": {
                    "a": {"description": "An integer value",
                          "type": "integer"},
                    "b": {"description": "An integer value",
                          "type": "integer"},
                },
                "required": ["a", "b"],
                "additionalProperties": False,
            },
            "strict": True,
        },
    }

    return schema

def tools():
    return [
        add_schema(),
        multiply_schema(),
    ]


def system_prompt():
    return "You are a helpful AI assistant with access to specialized tools."


## help methods
def call_function(name, args):
    # this can be better...
    if name == "add":
        return add(**args)
    elif name == "multiply":
        return multiply(**args)


def main():
   # formatted_tools = [convert_to_openai_tool(add),convert_to_openai_tool(multiply)]
   # print(json.dumps(formatted_tools, indent=4))



    model = load_chat_model()
    mytools = tools()
    messages = [
        {"role": "system", "content": system_prompt()},
        {"role": "user", "content": "What is 3+11?"},
    ]

    print("[user] -> ", messages[1]['content'])

    output = model.chat(
        messages=messages,
        tools=mytools,
        tool_choice_option="auto",
    )
    response = output['choices'][0]['message']
    print(response)
    ## tool calls
    tool_calls = response.get('tool_calls')
    if tool_calls is None:
        return "unexpected result"

    for tc in tool_calls:
        # add response to "memory"
        messages.append(response)
        name = tc['function']['name']
        args = json.loads(tc['function']['arguments'])
        result = call_function(name, args)
        # append the result
        messages.append(
            {"role": "tool", "name":name,"tool_call_id": tc['id'], "content": json.dumps(result)}
        )

    output = model.chat(
        messages=messages,
        tools=mytools,
        tool_choice_option="auto",
    )

    print("[agent] -> ", output['choices'][0]['message']['content'])

    messages.append(
        {"role": "user", "content": "What about 3*11?"},
    )

    output = model.chat(
        messages=messages,
        tools=mytools,
        tool_choice_option="auto",
    )
    response = output['choices'][0]['message']
    print(response)
    ## tool calls
    tool_calls = response.get('tool_calls')
    if tool_calls is None:
        return "unexpected result"

    for tc in tool_calls:
        # add response to "memory"
        messages.append(response)
        name = tc['function']['name']
        args = json.loads(tc['function']['arguments'])
        result = call_function(name, args)
        # append the result
        messages.append(
            {"role": "tool", "name": name, "tool_call_id": tc['id'], "content": json.dumps(result)}
        )

    output = model.chat(
        messages=messages,
        tools=mytools,
        tool_choice_option="auto",
    )

    print("[agent] -> ", output['choices'][0]['message']['content'])


if __name__ == "__main__":
    main()