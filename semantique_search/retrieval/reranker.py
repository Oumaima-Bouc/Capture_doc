from sentence_transformers import CrossEncoder


class Reranker:

    def __init__(self):

        print("Loading reranker model...")

        self.model = CrossEncoder(
            "BAAI/bge-reranker-base"
            # or "cross-encoder/ms-marco-MiniLM-L-6-v2"
        )

        print("Reranker loaded successfully!")

    def rerank(self, question, results, top_k=5):
        """
        Parameters
        ----------
        question : str

        results : list
            Output of pgvector search

        top_k : int

        Returns
        -------
        Reranked results
        """

        pairs = []

        for result in results:

            chunk_text = result[2]

            pairs.append((question, chunk_text))

        scores = self.model.predict(pairs)

        reranked = []

        for result, score in zip(results, scores):

            reranked.append((score, result))

        reranked.sort(
            key=lambda x: x[0],
            reverse=True
        )

        final_results = []

        for score, result in reranked[:top_k]:

            filename, chunk_number, chunk_text, distance = result

            final_results.append(
                (
                    filename,
                    chunk_number,
                    chunk_text,
                    distance,
                    score
                )
            )

        return final_results