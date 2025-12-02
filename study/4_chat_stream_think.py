from ollama import chat
from dotenv import load_dotenv
import os
load_dotenv()



stream = chat(
    model=os.getenv('model_name'),
    messages=[
        {"role" : "user", "content" : "how many letters are in the english alphabet?"}
    ],
    think=True,
    stream=True
)


in_thinking = False

for chunk in stream:
    if chunk.message.thinking and not in_thinking:
        in_thinking = True
        print("Thinking:\n", end='')

    if chunk.message.thinking:
        print(chunk.message.thinking, end='')
    elif chunk.message.content:
        if in_thinking:
            print(chunk.message.content, end='')
            in_thinking = False
        print(chunk.message.content, end='')