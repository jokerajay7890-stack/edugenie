from ai_client import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational material
for quick student revision.

Requirements:

- Keep important facts.
- Remove repetition.
- Use simple language.
- Use headings where useful.
- Use bullet points for important information.
- Do not add information that is not in the source.

Material:

{text}
"""

    return generate_text(
        prompt,
        system_instruction="""
You are EduGenie's study-summary assistant.

Create accurate and concise revision notes.
""",
        temperature=0.25,
        max_output_tokens=1800
    )