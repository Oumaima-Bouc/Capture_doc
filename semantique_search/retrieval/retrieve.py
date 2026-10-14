from retrieval.normalize_query import QueryNormalizer
from retrieval.embed_query import QueryEmbedder
from retrieval.search_pgvector import PgVectorSearcher
from retrieval.reranker import Reranker


class Retriever:

    def __init__(self):

        self.normalizer = QueryNormalizer()

        self.embedder = QueryEmbedder()

        self.searcher = PgVectorSearcher()

        self.reranker = Reranker()

    def search(self, question):

        normalized = self.normalizer.normalize(question)

        embedding = self.embedder.embed(normalized)

        candidates = self.searcher.search(
            embedding,
            top_k=20
        )

        results = self.reranker.rerank(
            normalized,
            candidates,
            top_k=5
        )

        return results