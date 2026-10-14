from retrieval.embed_query import QueryEmbedder
from retrieval.search_pgvector import PgVectorSearcher


embedder = QueryEmbedder()
searcher = PgVectorSearcher()

question = "What is an Artificial Neural Network?"

embedding = embedder.embed(question)

results = searcher.search(embedding)

print("=" * 60)
print("Search Results")
print("=" * 60)

for i, result in enumerate(results, start=1):

    filename, chunk_number, chunk_text, distance = result

    print(f"\nResult {i}")
    print(f"Document : {filename}")
    print(f"Chunk    : {chunk_number}")
    print(f"Distance : {distance:.4f}")
    print(f"Preview  : {chunk_text[:200]}")

searcher.close()