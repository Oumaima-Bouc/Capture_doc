class PromptBuilder:

    # ------------------------------------------
    # Build Context
    # ------------------------------------------

    def build_context(self, results):

        context = ""

        for result in results:

            filename, chunk_number, chunk_text, distance, score = result

            context += f"Document: {filename}\n"
            context += f"Chunk: {chunk_number}\n"
            context += chunk_text
            context += "\n\n"

        return context

    # ------------------------------------------
    # Build Prompt
    # ------------------------------------------

    def build_prompt(self, question, context):

        prompt = f"""
You are an AI assistant.

Answer ONLY using the provided context.

If the answer cannot be found in the context, reply exactly:

"I could not find the answer in the retrieved documents."

==============================
Context
==============================

{context}

==============================
Question
==============================

{question}

==============================
Answer
==============================
"""

        return prompt