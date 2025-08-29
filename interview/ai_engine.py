import os
import json
import re
import time
from openai import OpenAI  # ✅ new import

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DEFAULT_MODEL = "gpt-4o-mini"  # use a small/cheap model for dev; change in prod

def _extract_json_block(text: str):
    """
    Try to extract the first {...} JSON block from a text blob.
    Returns a dict or None.
    """
    if not text:
        return None
    m = re.search(r'(\{(?:.|\s)*\})', text, re.S)
    if not m:
        return None
    block = m.group(1)
    try:
        return json.loads(block)
    except json.JSONDecodeError:
        try:
            fixed = block.replace("'", '"')
            return json.loads(fixed)
        except Exception:
            return None

def ai_evaluate_answer(question_text: str, user_answer: str, model: str = DEFAULT_MODEL, max_retries: int = 1):
    """
    Call OpenAI to evaluate the candidate's answer.
    Returns a dict with keys: strengths (list), weaknesses (list),
    improvements (list), score (int 0-10), raw (raw text).
    Raises exceptions on final failure.
    """
    prompt = f"""
You are an expert interview coach. Evaluate the candidate's answer to the question.

Question:
{question_text}

Candidate's answer:
{user_answer}

INSTRUCTIONS (VERY IMPORTANT):
- RESPOND WITH VALID JSON ONLY.
- The JSON object must have these keys:
  {{
    "strengths": ["short positive points"],
    "weaknesses": ["short negative points"],
    "improvements": ["concise suggestions"],
    "score": 0
  }}
- `score` should be an integer between 0 and 10 (0 worst, 10 best).
- Keep each list to 1-6 short items maximum.
- Do NOT output any extra commentary outside the JSON.
"""

    for attempt in range(max_retries + 1):
        try:
            # ✅ updated call
            resp = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are a helpful, objective AI interviewer."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,
                max_tokens=400
            )

            content = resp.choices[0].message.content.strip()  # ✅ new access pattern

            try:
                parsed = json.loads(content)
            except json.JSONDecodeError:
                parsed = _extract_json_block(content)

            if not parsed:
                return {
                    "strengths": [],
                    "weaknesses": [],
                    "improvements": ["AI returned non-JSON response; see raw_ai_response."],
                    "score": 0,
                    "raw": content
                }

            score = parsed.get("score", 0)
            try:
                score = int(round(float(score)))
            except Exception:
                m = re.search(r"(\d+)", str(score))
                score = int(m.group(1)) if m else 0
            score = max(0, min(10, score))
            parsed["score"] = score
            parsed["raw"] = content
            return parsed

        except Exception as e:
            if attempt < max_retries:
                time.sleep(1 + attempt * 2)
                continue
            raise
