import os
from dotenv import load_dotenv
load_dotenv()

from app import config

print(f"GROQ_API_KEY env: {os.getenv('GROQ_API_KEY')[:20]}...")
print(f"LLM_PROVIDER: {config.LLM_PROVIDER}")
print(f"LLM_ENABLED: {config.LLM_ENABLED}")
print(f"SDK Check - groq importable: {config._sdk_importable('groq')}")
print(f"API Key check - groq has key: {config._api_key('groq') is not None}")
print(f"Provider selected: {config.llm_provider()}")
print(f"Model: {config.llm_model()}")
