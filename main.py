import os
import argparse
from dotenv import load_dotenv
from openai import OpenAI

from prompts import system_prompt
from call_function import available_functions
from functions.call_function import call_function

load_dotenv()

api_key = os.environ.get("OPENROUTER_API_KEY")
if not api_key:
    raise RuntimeError("Missing OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=api_key,
)

parser = argparse.ArgumentParser()
parser.add_argument("user_prompt")
parser.add_argument("--verbose", action="store_true")
args = parser.parse_args()

messages = [
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": args.user_prompt},
]

for _ in range(20):

    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )

    message = response.choices[0].message

    messages.append(message)

    if args.verbose:
        print(f"\nAssistant: {message}")

    if message.tool_calls:

        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, args.verbose)

            if not result_message.get("content"):
                raise Exception("Empty tool result")

            messages.append(result_message)

            if args.verbose:
                print("->", result_message["content"])

    else:
        print(message.content)
        break

else:
    print("Agent did not finish in 20 steps")
    exit(1)