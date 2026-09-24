from app.services.ai_service import AIService


class DocumentVerificationService:

    def __init__(self):
        self.ai_service = AIService()

    def verify(
        self,
        extracted_text: str,
        language: str = "en"
    ):
        # No OCR text
        if not extracted_text:
            return {
                "status": "FAILED",
                "result": "Document could not be read.",
                "missing_information": "Unable to extract text from document."
            }

        # Basic document verification
        prompt = f"""
You are a document verification assistant for Procedure Assist AI.

DOCUMENT TEXT:
{extracted_text}

PREFERRED LANGUAGE:
{language}

Analyze the document text and provide:

1. Whether the document appears readable and usable.
2. Important information found in the document.
3. Any clearly missing information.
4. Any obvious problem with the document.

Rules:
- Do not claim that the document is officially verified.
- Do not invent information.
- If something cannot be determined from the text, say so.
- Respond in the preferred language.
- Keep the explanation simple.
"""

        result = self.ai_service.generate(
            query="Verify this government document",
            context=extracted_text,
            language=language
        )

        return {
            "status": "REVIEW_REQUIRED",
            "result": result,
            "missing_information": "See verification result."
        }