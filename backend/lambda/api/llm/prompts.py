SYSTEM_PROMPT = """
You are an AI assistant that answers questions using only the provided document.

Rules:
- Answer only from the document content.
- If the answer is not in the document, say:
  "I couldn't find that information in the document."
- Keep responses clear and concise.
"""


def build_prompt(document: str, question: str) -> str:
    return f"""
{SYSTEM_PROMPT}

Document:
{document}

Question:
{question}
"""