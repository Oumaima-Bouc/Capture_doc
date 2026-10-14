from retrieval.reranker import Reranker

reranker = Reranker()

question = "What is an Artificial Neural Network?"

chunks = [
    "Artificial Neural Networks are models inspired by the human brain. They are used in machine learning.",
    "Computer security protects computers and networks against attacks.",
    "Walmart is one of the largest retail companies in the world."
]

results = reranker.rerank(question, chunks)

print("\nReranking Results")
print("=" * 60)

for i, (chunk, score) in enumerate(results, start=1):
    print(f"\nRank {i}")
    print(f"Score : {score:.4f}")
    print(f"Chunk : {chunk}")