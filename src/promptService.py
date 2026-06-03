import requests
from typing import List

class OllamaService:
    def __init__(self, base_url: str = "http://localhost:11434", model: str = "llama3"):
        self.base_url = base_url
        self.model = model
        self.endpoint = f"{self.base_url}/api/generate"

    def build_prompt(self, context: List[str], question: str) -> str:
        context_text = "\n".join(context)

        prompt = f"""
You are an AI assistant specialized in financing and banking.
Use the context below to answer the user clearly and accurately.

Context:
{context_text}

User question:
{question}
"""
        return prompt.strip()

    def generate(self, prompt: str) -> str:
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False
        }

        response = requests.post(self.endpoint, json=payload)

        if response.status_code != 200:
            raise Exception(f"Ollama error: {response.text}")

        data = response.json()

        if "response" in data:
            return data["response"]
        else:
            raise Exception(f"Unexpected response: {data}")

    def ask(self, context: List[str], question: str) -> str:
        prompt = self.build_prompt(context, question)
        return self.generate(prompt)