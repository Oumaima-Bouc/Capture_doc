import ollama

response = ollama.chat(
    model="mistral:latest",
    messages=[
        {
            "role": "user",
            "content": "What is Artificial Intelligence?"
        }
    ]
)

print(response["message"]["content"])