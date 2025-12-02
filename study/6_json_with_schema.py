from ollama import chat
from dotenv import load_dotenv
import os
import json
from pydantic import BaseModel
load_dotenv()

class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]


response = chat(
  model=os.getenv('model_name'),
  messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
  format=Country.model_json_schema(),
)

country = Country.model_validate_json(response.message.content)
print(country)

