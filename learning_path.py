from ai_client import generate_text


def get_learning_recommendations(
    topic: str,
    level: str = "beginner",
    weeks: int = 6
) -> str:

    prompt = f"""
Create a structured {weeks}-week learning plan.

Topic:
{topic}

Student level:
{level}

For every week include:

1. Topics to learn
2. Practical activity
3. Practice task
4. What to revise
5. Suggested resource type

Resource types can include:

- YouTube/video lessons
- Official documentation
- Books
- Practice websites
- Projects
- Exercises

Do not invent exact URLs.

At the end provide:

Milestone Checklist

Make the plan realistic for a college student.
"""

    return generate_text(
        prompt,
        system_instruction="""
You are an expert learning-path designer.

Create realistic, progressive,
student-friendly learning plans.
""",
        temperature=0.5,
        max_output_tokens=2800
    )