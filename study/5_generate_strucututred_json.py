from ollama import chat
from dotenv import load_dotenv
import os
import json
load_dotenv()

# response = chat(
#     model=os.getenv('model_name'),
#     messages=[
#         {"role" : "user", "content" : "List five programming languages and for each, provide its main use case in JSON format."}
#     ],
#     format='json'
# )

# print(json.dumps(response.message.content, indent=4))

from ollama import chat

response = chat(
  model=os.getenv('model_name'),
  messages=[{'role': 'user', 'content': 'Tell me about Canada.'}],
  format='json'
)
print(response.message.content)