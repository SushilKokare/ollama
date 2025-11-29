from ollama import chat
from dotenv import load_dotenv
import os
load_dotenv()



stream = chat(
    model=os.getenv('model_name'),
    messages=[
        {"role" : "user", "content" : "count from 1 to 13 just nothing else"}
    ],
    stream=True
)

in_thinking=False
content = ""
thinking = ""

for chunk in stream:
    # print(chunk)
    if chunk.message.thinking:
        if not in_thinking:
            in_thinking = True
            print("Thinking:\n", end="", flush=True)
        print(chunk.message.thinking, end="", flush=True)

        # accumulate the partial thinking
        thinking += chunk.message.thinking

    elif chunk.message.content:
        if in_thinking:
            in_thinking = False
            print("\nDone Thinking.\n", end="", flush=True)
            print("\n\n Answer:\n", end="", flush=True)
        print(chunk.message.content, end="", flush=True)

        # accumulate the partial content
        content += chunk.message.content

        # append the accumulated fields to the messages for the next request

        new_messages = [
            {"role" : "assistant", thinking: thinking, content: content}
        ]


# print("\n new_messages:\n", new_messages)