from retrieval.normalize_query import QueryNormalizer
from retrieval.embed_query import QueryEmbedder
from retrieval.search_pgvector import PgVectorSearcher
from retrieval.reranker import Reranker
from retrieval.threshold import SimilarityThreshold

from llm.prompt import PromptBuilder
from llm.generator import LLMGenerator

from utils.source_formatter import SourceFormatter


class SemanticSearch:

    def __init__(self):

        self.normalizer = QueryNormalizer()
        self.embedder = QueryEmbedder()
        self.searcher = PgVectorSearcher()

        self.reranker = Reranker()
        self.threshold = SimilarityThreshold(threshold=0.0)

        self.prompt_builder = PromptBuilder()
        self.generator = LLMGenerator()

        self.source_formatter = SourceFormatter()

    # ---------------------------------------------------
    # Step 1 - Normalize Query
    # ---------------------------------------------------

    def prepare_query(self, question):

        normalized_question = self.normalizer.normalize(question)

        print("\nNormalized Question:")
        print(normalized_question)

        return normalized_question

    # ---------------------------------------------------
    # Step 2 - Generate Embedding
    # ---------------------------------------------------

    def generate_embedding(self, normalized_question):

        embedding = self.embedder.embed(normalized_question)

        print("\nEmbedding generated successfully.")
        print(f"Embedding dimension: {len(embedding)}")

        return embedding

    # ---------------------------------------------------
    # Step 3 - Vector Search
    # ---------------------------------------------------

    def vector_search(self, embedding):

        return self.searcher.search(
            embedding,
            top_k=20
        )

    # ---------------------------------------------------
    # Step 4 - Rerank
    # ---------------------------------------------------

    def rerank_results(self, question, results):

        return self.reranker.rerank(
            question,
            results,
            top_k=5
        )

    # ---------------------------------------------------
    # Step 5 - Threshold
    # ---------------------------------------------------

    def apply_threshold(self, results):

        return self.threshold.apply(results)

    # ---------------------------------------------------
    # Display Results
    # ---------------------------------------------------

    def display_results(self, results, answer):

        print("\n" + "=" * 60)
        print("Top Matching Chunks (After Reranking)")
        print("=" * 60)

        if len(results) == 0:
            print("No relevant results found.")
            return

        for i, result in enumerate(results, start=1):

            filename, chunk_number, chunk_text, distance, score = result

            print(f"\nResult {i}")
            print(f"Document : {filename}")
            print(f"Chunk    : {chunk_number}")
            print(f"Score    : {score:.4f}")
            print(f"Distance : {distance:.4f}")
            print(f"Preview  : {chunk_text[:200]}...")

        print("\n" + "=" * 60)
        print("Answer")
        print("=" * 60)
        print(answer)

        print("\n" + "=" * 60)
        print("Sources")
        print("=" * 60)

        print(self.source_formatter.format(results))

    # ---------------------------------------------------
    # Complete Online Pipeline
    # ---------------------------------------------------

    def run(self, question):

        # Step 1
        normalized_question = self.prepare_query(question)

        # Step 2
        embedding = self.generate_embedding(normalized_question)

        # Step 3
        results = self.vector_search(embedding)

        # Step 4
        results = self.rerank_results(
            normalized_question,
            results
        )

        # Step 5
        results = self.apply_threshold(results)

        if len(results) == 0:

            print("\nNo relevant documents found.")
            return

        # Step 6 - Build Context
        context = self.prompt_builder.build_context(results)

# Step 7 - Build Prompt
        prompt = self.prompt_builder.build_prompt(
        normalized_question,
        context
        )

# Step 8 - Generate Answer
        answer = self.generator.generate(prompt)

# Step 9 - Display Results
        self.display_results(results, answer)
    # ---------------------------------------------------
    # Close Database
    # ---------------------------------------------------

    def close(self):

        self.searcher.close()