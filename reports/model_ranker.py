class ModelRanker:

    def rank(self, results):

        ranked = sorted(
            results,
            key=lambda x: x["composite_risk"]
        )

        print("\n=== Model Safety Ranking ===")

        for i, r in enumerate(ranked, start=1):

            print(
                f"{i}. {r['model']}  |  Risk: {r['composite_risk']}  |  Severity: {r['severity']}"
            )

        return ranked