"""Message prefilling and stop sequences and handling (semi-)structured data."""

from anthropic import Anthropic
from dotenv import load_dotenv
import json
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

def chat(messages, system_prompt=None, temperature=0.0, stop_sequences=None):
    """Chat with the math specialist model."""
    params = {
        "model": model,
        "max_tokens": 200,
        "messages": messages,
        "temperature": temperature,
        "stop_sequences": stop_sequences
    }

    if system_prompt:
        params["system"] = system_prompt
    
    message = client.messages.create(**params)

    return message.content[0].text


messages = []

add_user_message(messages, "Which is better, coffee or tea?")


# Message prefilling with Assistant message.
add_assistant_message(messages, "Coffee is better because")

# Using stop sequences
stop_seqs = ["5"]
add_user_message(messages, "Count to 10")
answer = chat(messages, stop_sequences=stop_seqs)
print(answer)


# Example for structured data generation
messages = []

add_user_message(messages, "Generate a very short event bridge rule as json.")
add_assistant_message(messages, "```json")

text = chat(messages, stop_sequences=["```"])
print(text)

json_obj = json.loads(text.strip())
print(json_obj)
