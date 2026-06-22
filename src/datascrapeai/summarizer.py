"""Module for summarizing text using Groq API."""

import os

from groq import Groq


def summarize_text(
    text: str,
    api_key: str | None = None,
    model: str = "gemma2-9b-it",
    max_input_chars: int = 10000,
    temperature: float = 0.3,
    max_tokens: int = 500,
) -> str:
    """Summarize the given text using Groq's API.

    Args:
        text: The text to summarize.
        api_key: Groq API key. If None, reads from GROQ_API_KEY env var.
        model: Model name to use (default gemma2-9b-it).
        max_input_chars: Maximum characters to send to the API.
        temperature: Sampling temperature.
        max_tokens: Maximum tokens in the response.

    Returns:
        The summary string.

    Raises:
        RuntimeError: If API key is missing or API call fails.
    """
    if api_key is None:
        api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        raise RuntimeError("GROQ_API_KEY environment variable not set.")

    client = Groq(api_key=api_key)

    prompt = f"Summarize the following text in a few sentences:\n\n{text[:max_input_chars]}"

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
        summary = chat_completion.choices[0].message.content.strip()
    except Exception as e:
        raise RuntimeError(f"Groq API error: {e}") from e

    return summary
