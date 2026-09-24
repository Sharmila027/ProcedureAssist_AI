from pydantic import BaseModel, Field


SUPPORTED_LANGUAGES = {
    "en": "English",
    "ta": "Tamil",
    "hi": "Hindi",
    "te": "Telugu",
    "kn": "Kannada",
    "ml": "Malayalam",
}


class QueryRequest(BaseModel):
    query: str = Field(min_length=1)
    language: str = "en"


class QueryResponse(BaseModel):
    procedure: str
    language: str
    answer: str
    steps: list[str]
    documents: list[str]
    sources: list[str]