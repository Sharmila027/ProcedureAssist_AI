class OutputService:

    def generate(
        self,
        answer: str,
        procedure: str,
        language: str,
        sources: list[str]
    ):

        return {
            "procedure": procedure,
            "language": language,
            "answer": answer,
            "steps": self.extract_steps(answer),
            "documents": self.extract_documents(answer),
            "sources": sources
        }

    def extract_steps(
        self,
        answer: str
    ):

        steps = []

        lines = answer.splitlines()

        for line in lines:

            line = line.strip()

            if not line:
                continue

            if (
                line[0:2].isdigit()
                and "." in line
            ):
                steps.append(
                    line.split(".", 1)[1].strip()
                )

        return steps

    def extract_documents(
        self,
        answer: str
    ):

        documents = []

        lines = answer.splitlines()

        for line in lines:

            lower = line.lower()

            if (
                "document" in lower
                or "certificate" in lower
                or "proof" in lower
            ):
                documents.append(
                    line.strip("- •")
                )

        return documents