import os

from llm.gemini import GeminiProvider


def get_llm_provider():
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()

    if provider == "gemini":
        return GeminiProvider()

    raise ValueError(f"Unsupported LLM provider: {provider}")