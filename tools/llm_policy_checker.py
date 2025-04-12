import json
import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")


def load_policies():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    policy_path = os.path.join(base_dir, "..", "policy_rag.json")
    with open(policy_path, "r") as f:
        return json.load(f)


def build_prompt(message, policies):
    policy_text = "\n".join(
        [
            f"- {p.get('article', p.get('category'))} | {p['title']} | Risk: {p['risk_level']} | Recommendation: {p['recommendation']} | Keywords: {', '.join(p['keywords'])}"
            for p in policies
        ]
    )

    return f"""
You are a compliance assistant reviewing internal communications for GDPR and social engineering risks.

Below are internal policies:

{policy_text}

---

Now, assess the following message:

"{message}"

Respond in **JSON format** with the following fields only:
- matched_policy (string)
- article_or_category (string)
- risk_level (string)
- recommendation (string)
- confidence (float from 0 to 1)
- reason (string explanation of what triggered the match)

Only return valid JSON. Do not include any prose or markdown.
"""


def check_llm_policy_match(message: str) -> dict:
    policies = load_policies()
    prompt = build_prompt(message, policies)

    try:
        response = model.generate_content(prompt)
        raw = response.text

        # Attempt to clean up and parse response
        json_start = raw.find("{")
        json_end = raw.rfind("}") + 1
        cleaned = raw[json_start:json_end]

        result = json.loads(cleaned)

        return {
            "matched_policy": result.get("matched_policy"),
            "article": result.get("article_or_category"),
            "risk_level": result.get("risk_level"),
            "recommendation": result.get("recommendation"),
            "confidence": float(result.get("confidence", 0)),
            "risk_reason": result.get("reason"),
        }

    except Exception as e:
        return {
            "matched_policy": None,
            "article": None,
            "risk_level": None,
            "recommendation": "log_only",
            "confidence": 0.0,
            "risk_reason": f"Failed to parse LLM output: {e}"
        }
