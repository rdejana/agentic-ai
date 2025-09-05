import os
from ibm_watsonx_ai.foundation_models.schema import TextChatParameters
from ibm_watsonx_ai.foundation_models import ModelInference
from ibm_watsonx_ai import Credentials
from dotenv import load_dotenv

load_dotenv()  #load

def load_chat_model(model_id="",max_tokens=1024,temperature=1):
    if model_id == "" :
        model_id = os.getenv("MODEL_ID")

    project_id = os.getenv("WX_PROJECT_ID")
    credentials = Credentials(
        url=os.getenv("WX_URL"),
        api_key=os.getenv("WX_API_KEY"),
    )

    params = TextChatParameters(
        max_tokens=max_tokens,
        temperature=temperature
    )

    model = ModelInference(
        model_id=model_id,
        credentials=credentials,
        project_id=project_id,
        params=params
    )

    return model
