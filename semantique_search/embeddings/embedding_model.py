import os
import json

from sentence_transformers import SentenceTransformer


class EmbeddingGenerator:

    def __init__(self):

        self.model = SentenceTransformer(
            "BAAI/bge-small-en-v1.5"
        )

    def generate(self, chunks):

        embeddings = []

        for chunk in chunks:

            vector = self.model.encode(
                chunk["text"],
                normalize_embeddings=True
            )

            embeddings.append({
                "document_name": chunk["document_name"],
                "chunk_id": chunk["chunk_id"],
                "text": chunk["text"],
                "embedding": vector.tolist()
            })

        return embeddings


def save_embeddings(embeddings, output_folder, filename):

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(
            embeddings,
            f,
            indent=4,
            ensure_ascii=False
        )

    return output_path