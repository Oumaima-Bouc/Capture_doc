import re


class QueryNormalizer:

    def normalize(self, query: str) -> str:
        """
        Normalize the user's question while preserving its meaning.
        """

        # Remove leading/trailing whitespace
        query = query.strip()

        # Replace tabs/newlines/multiple spaces with a single space
        query = re.sub(r"\s+", " ", query)

        # Remove spaces before punctuation
        query = re.sub(r"\s+([?.!,;:])", r"\1", query)

        # Replace multiple punctuation marks with one
        query = re.sub(r"\?{2,}", "?", query)
        query = re.sub(r"!{2,}", "!", query)
        query = re.sub(r"\.{2,}", ".", query)
        query = re.sub(r",{2,}", ",", query)

        # Remove repeated commas mixed with spaces
        query = re.sub(r",\s*,+", ",", query)

        # Convert to lowercase
        query = query.lower()

        return query