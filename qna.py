from ai_client import generate_text


SYSTEM_INSTRUCTION = """
You are EduGenie, a friendly AI educational assistant.

Your job is to help students understand academic topics.

Rules:

1. Answer accurately.
2. Use simple language.
3. Explain difficult ideas step-by-step.
4. Give examples when useful.
5. Do not make up facts.
6. If something is uncertain, clearly say so.
"""


def answer_question(question: str) -> str:

    prompt = f"""
Answer the student's question clearly.

Student Question:

{question}

Give a useful educational answer.
"""

    return generate_text(
        prompt,
        system_instruction=SYSTEM_INSTRUCTION,
        temperature=0.3,
        max_output_tokens=1200
    )