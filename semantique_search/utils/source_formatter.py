class SourceFormatter:

    def format(self, results):

        if not results:
            return "No sources found."

        output = "\nSources\n"
        output += "-" * 50 + "\n"

        for i, result in enumerate(results, start=1):

            filename, chunk_number, chunk_text, distance, score = result

            output += (
                f"[{i}] {filename}\n"
                f"    Chunk: {chunk_number}\n"
                f"    Reranker Score: {score:.4f}\n\n"
            )

        return output