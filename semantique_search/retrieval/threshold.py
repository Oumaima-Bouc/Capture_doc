class SimilarityThreshold:

    def __init__(self, threshold=0.0):

        self.threshold = threshold

    def apply(self, results):

        filtered = []

        for result in results:

            filename, chunk_number, chunk_text, distance, score = result

            if score >= self.threshold:

                filtered.append(result)

        return filtered