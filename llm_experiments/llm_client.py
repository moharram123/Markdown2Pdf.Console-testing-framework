# llm_experiments/llm_client.py
"""
LLM client for the optional exploratory prototype.
Requires OPENAI_API_KEY to be set in the environment or a local .env file.
Run manually — never imported by the core test suite.
"""
import os
import time

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def ask_llm(prompt: str) -> str:
    """Send a prompt to OpenAI gpt-4o-mini and return the response text."""
    time.sleep(1)  # basic rate-limit guard
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content