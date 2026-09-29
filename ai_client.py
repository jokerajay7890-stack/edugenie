import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types


load_dotenv()


MODEL_NAME = os.getenv(
    "GEMINI_MODEL",
    "gemini-3.6-flash"
)


@lru_cache(maxsize=1)
def get_client():

    api_key = os.getenv(
        "GEMINI_API_KEY"
    )

    if not api_key:

        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Create a .env file and add your Gemini API key."
        )

    return genai.Client(
        api_key=api_key
    )


def generate_text(
    prompt: str,
    *,
    system_instruction: str | None = None,
    temperature: float = 0.4,
    max_output_tokens: int = 2048,
    response_mime_type: str | None = None
) -> str:

    config = types.GenerateContentConfig(
        temperature=temperature,
        max_output_tokens=max_output_tokens
    )

    if system_instruction:

        config.system_instruction = (
            system_instruction
        )

    if response_mime_type:

        config.response_mime_type = (
            response_mime_type
        )

    response = get_client().models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=config
    )

    text = response.text

    if not text:

        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return text.strip()