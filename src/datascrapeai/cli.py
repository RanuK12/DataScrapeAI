"""Command-line interface for DataScrapeAI."""

import argparse
import json
import sys
from datetime import datetime, timezone

from .scraper import scrape_url
from .summarizer import summarize_text
from .utils import sanitize_filename


def main():
    parser = argparse.ArgumentParser(
        prog="datascrapeai",
        description="Scrape a web page and summarize its content using Groq API.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # scrape subcommand
    scrape_parser = subparsers.add_parser("scrape", help="Scrape a URL and save to JSON")
    scrape_parser.add_argument("url", help="URL to scrape")
    scrape_parser.add_argument(
        "-o", "--output",
        help="Output JSON file (default: auto-generated from URL)",
    )

    # summarize subcommand
    summarize_parser = subparsers.add_parser("summarize", help="Summarize a scraped JSON file")
    summarize_parser.add_argument("input", help="Input JSON file (from scrape)")
    summarize_parser.add_argument(
        "-o", "--output",
        help="Output JSON file (default: input file with _summary suffix)",
    )

    args = parser.parse_args()

    if args.command == "scrape":
        try:
            data = scrape_url(args.url)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        if args.output:
            out_path = args.output
        else:
            safe_name = sanitize_filename(args.url)
            out_path = f"{safe_name}.json"

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

        print(f"Saved to {out_path}")

    elif args.command == "summarize":
        try:
            with open(args.input, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error reading {args.input}: {e}", file=sys.stderr)
            sys.exit(1)

        text = data.get("text", "")
        if not text:
            print("No text found in JSON.", file=sys.stderr)
            sys.exit(1)

        try:
            summary = summarize_text(text)
        except RuntimeError as e:
            print(f"Error: {e}", file=sys.stderr)
            sys.exit(1)

        result = {
            "url": data.get("url"),
            "title": data.get("title"),
            "summary": summary,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        }

        if args.output:
            out_path = args.output
        else:
            out_path = args.input.replace(".json", "_summary.json")

        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"Summary saved to {out_path}")


if __name__ == "__main__":
    main()
