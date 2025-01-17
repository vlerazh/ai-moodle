# config.py

import os
from dotenv import load_dotenv
from openai import OpenAI

#Load .env
load_dotenv()

# Initialize OpenAI client
client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)
