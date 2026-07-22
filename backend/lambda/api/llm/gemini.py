from google import genai

from config import Config
from llm.base import BaseLLMProvider
from llm.prompts import build_prompt


class GeminiProvider(BaseLLMProvider):
    MODEL = "gemini-3.5-flash-lite"

    def ask(self, document: str, question: str) -> str:
        api_key = Config.get_gemini_api_key()

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured.")

        try:
            client = genai.Client(api_key=api_key)

            prompt = build_prompt(document, question)

            response = client.models.generate_content(
                model=self.MODEL,
                contents=prompt,
            )

            return response.text.strip()

        except Exception as e:
            raise RuntimeError(f"Gemini request failed: {str(e)}") from e