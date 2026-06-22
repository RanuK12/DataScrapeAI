#!/usr/bin/env python3
"""Load scraped JSON, summarize via Groq (Gemini model), save summary."""

import sys
import json
import os
from datetime import datetime, timezone

from groq import Groq

def main():
    if len(sys.argv) < 2:
        print("Usage: python summarizer.py <input.json>", file=sys.stderr)
        sys.exit(1)

    input_path = sys.argv[1]

    try:
        with open(input_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error reading {input_path}: {e}", file=sys.stderr)
        sys.exit(1)

    text = data.get("text", "")
    if not text:
        print("No text found in JSON.", file=sys.stderr)
        sys.exit(1)

    api_key = os.environ.get("GROQ_API_KEY")
    if not api_key:
        print("Error: GROQ_API_KEY environment variable not set.", file=sys.stderr)
        sys.exit(1)

    client = Groq(api_key=api_key)

    prompt = f"Summarize the following text in a few sentences:\n\n{text[:10000]}"  # limit length

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {"role": "user", "content": prompt},
            ],
            model="gemma2-9b-it",  # or "llama3-70b-8192"
            temperature=0.3,
            max_tokens=500,
        )
        summary = chat_completion.choices[0].message.content.strip()
    except Exception as e:
        print(f"Groq API error: {e}", file=sys.stderr)
        sys.exit(1)

    result = {
        "url": data.get("url"),
        "title": data.get("title"),
        "summary": summary,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }

    out_path = input_path.replace(".json", "_summary.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, ensure_ascii=False)

    print(f"Summary saved to {out_path}")

if __name__ == "__main__":
    main()
