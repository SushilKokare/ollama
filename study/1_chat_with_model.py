from ollama import chat
from ollama import ChatResponse
import os
from dotenv import load_dotenv

load_dotenv()

response: ChatResponse = chat(
    model=os.getenv('model_name'),
    messages=[
        {
            'role': 'user',
            'content': 'what is 2+1?'
        },
    ])

print('--------------------------')
print(type(response))
print('--------------------------')
print(response)
print('--------------------------')
print(response.message)
print('--------------------------')
print(response.message.content)
print('--------------------------')
print(response['message']['content'])
print('--------------------------')