from sentence_transformers import SentenceTransformer


class QueryEmbedder:

    def __init__(self):

        self.model = SentenceTransformer("BAAI/bge-small-en-v1.5")

    def embed(self, query):

        embedding = self.model.encode(query)

        return embedding.tolist()