class ClassificationService:

    def classify(self, results):
        if not results:
            return {
                "procedure": "Unknown",
                "code": None,
                "confidence": 0
            }

        best_result = results[0]

        metadata = best_result.get(
            "metadata",
            {}
        )

        distance = best_result.get(
            "distance",
            1
        )

        # Chroma distance is used only as a simple
        # retrieval confidence indicator.
        confidence = max(
            0,
            min(
                1,
                1 - distance
            )
        )

        return {
            "procedure": metadata.get(
                "service_name",
                "Government Procedure"
            ),
            "code": metadata.get("code"),
            "confidence": round(
                confidence,
                2
            )
        }