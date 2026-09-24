import re


class PreprocessingService:

    def clean_query(self, query: str) -> str:
        query = query.strip()

        query = re.sub(
            r"\s+",
            " ",
            query
        )

        return query

    def preprocess(
        self,
        query: str,
        language: str
    ):
        cleaned_query = self.clean_query(query)

        return {
            "original_query": query,
            "cleaned_query": cleaned_query,
            "language": language
        }