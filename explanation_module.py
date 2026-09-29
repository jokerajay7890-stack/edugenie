from ai_client import generate_text


def explain_topic(
    topic: str,
    level: str = "beginner"
) -> str:

    prompt = f"""
Explain the following topic to a {level}-level student.

Topic:
{topic}

Use this structure:

1. Simple definition
2. How it works
3. Easy example
4. Real-world example
5. Key points to remember

Keep the explanation clear and educational.
Avoid unnecessary complexity.
"""

    return generate_text(
        prompt,
        system_instruction="""
You are EduGenie, a patient teacher.

Explain difficult concepts in a way
that students can easily understand.
""",
        temperature=0.35,
        max_output_tokens=1600
    )