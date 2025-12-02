from ollama import chat
from dotenv import load_dotenv
from pydantic import BaseModel, ValidationError
import os
import re
import json

load_dotenv()


# -----------------------------
# 1. Your Schema
# -----------------------------
class Country(BaseModel):
    name: str
    capital: str
    languages: list[str]


# -----------------------------
# 2. Extract JSON from text
# -----------------------------
def extract_json(text: str) -> str:
    # ```json ... ```
    match = re.search(r"```json(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # any ``` ... ```
    match = re.search(r"```(.*?)```", text, re.DOTALL)
    if match:
        return match.group(1).strip()

    # { ... }
    match = re.search(r"\{.*\}", text, re.DOTALL)
    if match:
        return match.group(0).strip()

    raise ValueError("No JSON found in model output.")


# -----------------------------
# 3. Auto-fixer for schema mismatch
# -----------------------------
def fix_json_for_country(data: dict) -> dict:
    """
    Fix common issues:
    - languages returned as dict → convert to list of titles
    - languages returned as objects → convert to string list
    """
    fixed = {}

    # name
    fixed["name"] = str(data.get("name", ""))

    # capital
    fixed["capital"] = (
        data.get("capital")[0]
        if isinstance(data.get("capital"), list)
        else str(data.get("capital", ""))
    )

    # languages
    langs = data.get("languages", [])

    if isinstance(langs, dict):
        # dict → list of values → get titles
        fixed["languages"] = [v.get("title", str(v)) for k, v in langs.items()]

    elif isinstance(langs, list):
        cleaned = []
        for val in langs:
            if isinstance(val, str):
                cleaned.append(val)
            elif isinstance(val, dict):
                cleaned.append(val.get("title", str(val)))
            else:
                cleaned.append(str(val))
        fixed["languages"] = cleaned
    else:
        fixed["languages"] = [str(langs)]

    return fixed


# -----------------------------
# 4. Combined safe chat + validate
# -----------------------------
def safe_json_chat(model: str, schema_model, prompt: str):
    final_prompt = f"""
Return ONLY pure JSON.

It MUST match exactly this Python schema:

class Country:
    name: string
    capital: string
    languages: list of strings

RULES:
- Output only JSON.
- NO code fences.
- NO markdown.
- NO explanations.
- languages must be an ARRAY of STRINGS.
- capital must be a STRING, NOT a list.
"""

    response = chat(
        model=model,
        messages=[
            {"role": "user", "content": final_prompt + "\n" + prompt}
        ],
    )

    raw = response.message.content
    print("\n--- RAW OUTPUT ---")
    print(raw)

    # extract JSON block
    json_text = extract_json(raw)
    print("\n--- EXTRACTED JSON ---")
    print(json_text)

    # parse json to python dict
    data = json.loads(json_text)

    # auto fix schema mismatch
    fixed = fix_json_for_country(data)
    print("\n--- FIXED JSON ---")
    print(fixed)

    # validate with pydantic
    validated = schema_model(**fixed)

    return validated


# -----------------------------
# 5. Run test
# -----------------------------
if __name__ == "__main__":
    model_name = os.getenv("model_name")

    result = safe_json_chat(
        model=model_name,
        schema_model=Country,
        prompt="Tell me about Canada."
    )

    print("\n--- FINAL RESULT ---")
    print(result)
