"""AI evaluation — faithfulness, relevance, hallucination, and response quality scoring."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class EvaluationResult:
    metric: str
    score: float
    passed: bool
    details: str = ""


class FaithfulnessEvaluator:
    """Checks if the answer is grounded in the context."""

    def evaluate(self, answer: str, context: str) -> EvaluationResult:
        answer_words = set(w.lower() for w in answer.split() if len(w) > 3)
        context_words = set(w.lower() for w in context.split() if len(w) > 3)

        if not answer_words:
            return EvaluationResult("faithfulness", 0.0, False, "Empty answer")

        overlap = len(answer_words & context_words)
        score = overlap / len(answer_words)

        return EvaluationResult(
            "faithfulness",
            score,
            passed=score >= 0.3,
            details=f"Word overlap: {overlap}/{len(answer_words)} ({score:.2%})",
        )


class RelevanceEvaluator:
    """Checks if the answer is relevant to the question."""

    def evaluate(self, question: str, answer: str) -> EvaluationResult:
        question_keywords = set(w.lower() for w in question.split() if len(w) > 2)
        answer_keywords = set(w.lower() for w in answer.split() if len(w) > 2)

        if not question_keywords:
            return EvaluationResult("relevance", 0.0, False, "Empty question")

        overlap = len(question_keywords & answer_keywords)
        score = overlap / len(question_keywords)

        return EvaluationResult(
            "relevance",
            score,
            passed=score >= 0.2,
            details=f"Keyword overlap: {overlap}/{len(question_keywords)} ({score:.2%})",
        )


class HallucinationEvaluator:
    """Detects unsubstantiated claims in the answer."""

    def evaluate(self, answer: str, context: str) -> EvaluationResult:
        # Simple check: find claims not supported by context
        claims = [s.strip() for s in answer.split(".") if len(s.strip()) > 20]
        unsupported = 0

        for claim in claims:
            claim_words = set(w.lower() for w in claim.split() if len(w) > 3)
            context_words = set(w.lower() for w in context.split() if len(w) > 3)
            overlap = len(claim_words & context_words) / max(len(claim_words), 1)
            if overlap < 0.2:
                unsupported += 1

        total = max(len(claims), 1)
        score = 1.0 - (unsupported / total)

        return EvaluationResult(
            "hallucination",
            score,
            passed=score >= 0.7,
            details=f"Unsupported claims: {unsupported}/{len(claims)}",
        )


class PrecisionEvaluator:
    """Measures how many retrieved documents were useful."""

    def evaluate(self, retrieved: list, relevant: list) -> EvaluationResult:
        if not retrieved:
            return EvaluationResult("precision", 0.0, False, "No documents retrieved")

        retrieved_set = set(retrieved)
        relevant_set = set(relevant)

        if not relevant_set:
            return EvaluationResult("precision", 1.0, True, "No relevant docs expected")

        true_positives = len(retrieved_set & relevant_set)
        score = true_positives / len(retrieved_set)

        return EvaluationResult(
            "precision",
            score,
            passed=score >= 0.5,
            details=f"Precision: {true_positives}/{len(retrieved_set)} ({score:.2%})",
        )


class Evaluator:
    """Combined evaluation suite."""

    def __init__(self):
        self.faithfulness = FaithfulnessEvaluator()
        self.relevance = RelevanceEvaluator()
        self.hallucination = HallucinationEvaluator()
        self.precision = PrecisionEvaluator()

    def evaluate_all(self, question: str, answer: str, context: str) -> dict[str, EvaluationResult]:
        return {
            "faithfulness": self.faithfulness.evaluate(answer, context),
            "relevance": self.relevance.evaluate(question, answer),
            "hallucination": self.hallucination.evaluate(answer, context),
        }

    def overall_score(self, results: dict[str, EvaluationResult]) -> float:
        if not results:
            return 0.0
        return sum(r.score for r in results.values()) / len(results)
