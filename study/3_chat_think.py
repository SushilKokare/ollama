from ollama import chat
from dotenv import load_dotenv
import os
load_dotenv()



response = chat(
    model=os.getenv('model_name'),
    messages=[
        {"role" : "user", "content" : "how many letters are in the english alphabet?"}
    ],
    think=True,
    stream=False
)

print("Thinking:\n", response.message.thinking)
print("\n\n Answer:\n", response.message.content)