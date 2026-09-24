from app.schemas.query import SUPPORTED_LANGUAGES


class LanguageService:

    def is_supported(self, language: str) -> bool:
        return language in SUPPORTED_LANGUAGES

    def get_language_name(self, language: str) -> str:
        return SUPPORTED_LANGUAGES.get(
            language,
            "English"
        )

    def validate(self, language: str) -> str:
        language = language.lower().strip()

        if not self.is_supported(language):
            return "en"

        return language