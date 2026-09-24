import ollama


class AIService:

    def __init__(self):
        self.model = "qwen3:8b"

    def generate(
        self,
        query: str,
        context: str,
        language: str
    ):

        prompt = f"""
You are Procedure Assist AI, an AI assistant that helps citizens
understand government procedures.

USER QUERY:
{query}

GOVERNMENT SERVICE INFORMATION:
{context}

PREFERRED LANGUAGE:
{language}

RULES:
- Respond in the preferred language.
- Use only the government information provided above.
- Do not invent fees, documents, deadlines, authorities, or procedures.
- Explain the relevant service clearly and simply.
- Include useful information such as documents, fees, SLA,
  access method, and workflow when available.
- If the information is not available in the provided context,
  say that the available information is insufficient.
- Do not claim that you completed an application for the citizen.

Give a concise, helpful response.
"""

        response = ollama.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]