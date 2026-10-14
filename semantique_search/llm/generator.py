from ollama import Client


class LLMGenerator:

    def __init__(self):

        self.client = Client(host="http://127.0.0.1:11434")
        self.model = "mistral:latest"

    def generate(self, prompt):

        response = self.client.chat(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]