from app.services.retrieval_service import RetrievalService
from app.services.ai_service import AIService


class DocumentAnalysisService:

    def __init__(self):
        self.retrieval_service = RetrievalService()
        self.ai_service = AIService()

    def analyze(
        self,
        extracted_text: str,
        language: str = "en"
    ):
        # Check whether OCR extracted anything
        if not extracted_text:
            return {
                "status": "FAILED",
                "answer": "No readable text was found in the document.",
                "sources": []
            }

        # Search government knowledge base
        results = self.retrieval_service.search(
            extracted_text,
            limit=3
        )

        # No matching procedure
        if not results:
            return {
                "status": "NOT_FOUND",
                "answer": "No relevant government procedure was found for this document.",
                "sources": []
            }

        # Build AI context
        context = "\n\n".join(
            result["document"]
            for result in results
        )

        # Generate explanation
        answer = self.ai_service.generate(
            query=extracted_text,
            context=context,
            language=language
        )

        # Collect sources
        sources = []

        for result in results:
            source = result["metadata"].get("source")

            if source and source not in sources:
                sources.append(source)

        return {
            "status": "ANALYZED",
            "answer": answer,
            "sources": sources
        }