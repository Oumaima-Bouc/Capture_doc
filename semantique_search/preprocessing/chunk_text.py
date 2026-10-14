import json
import os


class TextChunker:

    def __init__(self, chunk_size=500, overlap=100):

        self.chunk_size = chunk_size
        self.overlap = overlap

    def chunk(self, text):

        words = text.split()

        chunks = []

        start = 0

        chunk_id = 1

        while start < len(words):

            end = start + self.chunk_size

            chunk_words = words[start:end]

            chunk_text = " ".join(chunk_words)

            chunks.append(
                {
                    "chunk_id": chunk_id,
                    "start_word": start,
                    "end_word": min(end, len(words)),
                    "text": chunk_text
                }
            )

            chunk_id += 1

            start += self.chunk_size - self.overlap

        return chunks


def save_chunks(chunks, output_folder, filename):

    os.makedirs(output_folder, exist_ok=True)

    output_path = os.path.join(output_folder, filename)

    with open(output_path, "w", encoding="utf-8") as f:

        json.dump(chunks, f, indent=4, ensure_ascii=False)

    return output_path