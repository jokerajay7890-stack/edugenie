import json

from ai_client import generate_text


def clean_json_block(raw: str) -> str:

    text = raw.strip()

    if text.startswith("```"):

        lines = text.splitlines()

        if lines:
            lines = lines[1:]

        if lines and lines[-1].strip() == "```":
            lines = lines[:-1]

        text = "\n".join(lines).strip()

    return text


def generate_quiz(
    text: str,
    count: int = 3
) -> list[dict]:

    prompt = f"""
Create exactly {count} multiple-choice questions
from the study material below.

Rules:

- Create exactly {count} questions.
- Every question must have exactly 4 options.
- Only one option should be correct.
- The answer must exactly match one option.
- Questions must be based only on the supplied material.
- Include a short explanation.

Return ONLY valid JSON.

Required format:

[
  {{
    "question": "Question",
    "options": [
      "Option A",
      "Option B",
      "Option C",
      "Option D"
    ],
    "answer": "Correct option",
    "explanation": "Why this answer is correct"
  }}
]

Study material:

{text}
"""

    raw = generate_text(
        prompt,
        system_instruction="""
You are an educational quiz generator.

Create fair and useful MCQs
based strictly on the provided study material.
""",
        temperature=0.35,
        max_output_tokens=3000,
        response_mime_type="application/json"
    )

    try:

        data = json.loads(
            clean_json_block(raw)
        )

    except json.JSONDecodeError as exc:

        raise RuntimeError(
            f"Quiz JSON could not be parsed: {exc}"
        )

    if not isinstance(data, list):

        raise RuntimeError(
            "Quiz response was not a list."
        )

    if len(data) != count:

        raise RuntimeError(
            f"Expected {count} questions, "
            f"but received {len(data)}."
        )

    cleaned = []

    for item in data:

        if not isinstance(item, dict):

            raise RuntimeError(
                "Invalid quiz question."
            )

        question = item.get(
            "question",
            ""
        )

        options = item.get(
            "options",
            []
        )

        answer = item.get(
            "answer",
            ""
        )

        explanation = item.get(
            "explanation",
            ""
        )

        if len(options) != 4:

            raise RuntimeError(
                "Every question must have 4 options."
            )

        if answer not in options:

            raise RuntimeError(
                "Quiz answer does not match an option."
            )

        cleaned.append(
            {
                "question": str(question),
                "options": [
                    str(option)
                    for option in options
                ],
                "answer": str(answer),
                "explanation": str(explanation)
            }
        )

    return cleaned