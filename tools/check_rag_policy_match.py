import json
import re
from typing import Optional, Tuple, Dict

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


with open("policy_rag.json", "r") as f:
    policies = json.load(f)


def clean_text(text: str) -> str:
    """Preprocess text for better matching."""
    return text.lower().strip()


def keyword_match(message: str, keywords: list[str]) -> int:
    """Simple keyword match count."""
    return sum(1 for kw in keywords if kw.lower() in message.lower())


def example_similarity(message: str, examples: list[str]) -> float:
    """Semantic similarity to examples using TF-IDF + cosine."""
    if not examples:
        return 0.0
    texts = [message] + examples
    vectorizer = TfidfVectorizer().fit_transform(texts)
    vectors = vectorizer.toarray()
    cosine_matrix = cosine_similarity([vectors[0]], vectors[1:])
    return float(max(cosine_matrix[0]))


def check_rag_policy_match(message: str) -> Optional[Dict[str, str]]:
    """Return matched policy info or None."""
    message = clean_text(message)

    best_score = 0
    best_match = None

    for policy in policies:
        keywords = policy.get("keywords", [])
        examples = policy.get("examples", [])

        keyword_score = keyword_match(message, keywords)
        example_score = example_similarity(message, examples)

        score = keyword_score * 2 + example_score * 100

        if score > best_score and (keyword_score > 0 or example_score > 0.2):
            best_score = score
            best_match = {
                "matched_policy": policy.get("title"),
                "article": policy.get("article", policy.get("category")),
                "risk_level": policy["risk_level"],
                "recommendation": policy["recommendation"],
                "confidence": round(min(score / 100, 1.0), 2),
                "risk_reason": f"Matched {keyword_score} keyword(s), example similarity {round(example_score, 2)}"
            }

    return best_match
