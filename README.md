# DataScrapeAI

CLI Scraper + AI Summarizer

Minimal tool to scrape a web page and summarize its content using Groq's API.

## Project Structure

```
datascrapeai/
├── src/
│   └── datascrapeai/
│       ├── __init__.py
│       ├── cli.py          # argparse entry point
│       ├── scraper.py      # scrape_url()
│       ├── summarizer.py   # summarize_text()
│       └── utils.py        # helpers (USER_AGENTS, sanitize_filename, extract_text)
├── tests/
│   └── test_utils.py
├── pyproject.toml
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

1. Install the package in editable mode:

   ```bash
   pip install -e .
   ```

2. Get a Groq API key from [console.groq.com](https://console.groq.com) and set it as an environment variable:

   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

## Usage

### Scrape a URL

```bash
python -m datascrapeai scrape <url>
```

This will create a JSON file (e.g., `example.com.json`) containing the page title, extracted text, and metadata.

### Summarize the scraped content

```bash
python -m datascrapeai summarize <output>.json
```

This will read the JSON file, send the text to Groq's model, and save a summary to `<output>_summary.json`.

### Full pipeline

```bash
python -m datascrapeai scrape https://example.com && python -m datascrapeai summarize example.com.json
```

## Notes

- The scraper uses rotating user‑agents to avoid simple blocks.
- The summarizer limits input to the first 10,000 characters.
- The default model is `gemma2-9b-it`. You can change it in `src/datascrapeai/summarizer.py`.
- Run tests with `pytest tests/`.
