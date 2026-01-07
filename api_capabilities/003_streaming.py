"""Focus on the importance and use of system prompts and temperature."""

from anthropic import Anthropic
from dotenv import load_dotenv
import os

_ = load_dotenv(override=True)

client = Anthropic()
model = os.getenv("CLAUDE_MODEL")


def add_user_message(messages, text):
    user_message = {"role": "user", "content": text}
    messages.append(user_message)

def add_assistant_message(messages, text):
    assistant_message = {"role": "assistant", "content": text}
    messages.append(assistant_message)

def chat(messages, system_prompt=None, temperature=0.0):
    """Chat with the math specialist model."""
    params = {
        "model": model,
        "max_tokens": 200,
        "messages": messages,
        "temperature": temperature
    }

    if system_prompt:
        params["system"] = system_prompt
    
    message = client.messages.create(**params)

    return message.content[0].text


messages = []

add_user_message(messages, "Write a 1 sentence description of a fake database.")

# stream = client.messages.create(
#     model=model,
#     max_tokens=100,
#     messages=messages,
#     stream=True
# )

# for event in stream:
#     chunk = event.content[0].text
#     print(chunk, end="", flush=True)

# Another implementation

with client.messages.stream(
    model=model,
    max_tokens=100,
    messages=messages
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)