from database.postgres_db import PostgreSQLDatabase


class PgVectorSearcher:
    """
    Search the PostgreSQL + pgvector database
    using a query embedding.
    """

    def __init__(self):
        self.db = PostgreSQLDatabase()

    def search(self, query_embedding, top_k=5):
        """
        Search for the most similar chunks.

        Parameters
        ----------
        query_embedding : list[float]
            Embedding of the user's question.

        top_k : int
            Number of results to return.

        Returns
        -------
        list
            List of tuples:
            (
                filename,
                chunk_number,
                chunk_text,
                distance
            )
        """

        # Convert Python list -> pgvector format
        vector = "[" + ",".join(map(str, query_embedding)) + "]"

        query = """
        SELECT
            d.filename,
            c.chunk_number,
            c.chunk_text,
            e.embedding <=> %s::vector AS distance
        FROM embeddings e
        JOIN chunks c
            ON e.chunk_id = c.id
        JOIN documents d
            ON c.document_id = d.id
        ORDER BY e.embedding <=> %s::vector
        LIMIT %s;
        """

        results = self.db.fetch_all(
            query,
            (
                vector,
                vector,
                top_k
            )
        )

        return results

    def close(self):
        """
        Close the database connection.
        """
        self.db.close()