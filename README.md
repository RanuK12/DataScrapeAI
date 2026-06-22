# DataScrapeAI# CLI Scraper + AI Summarizer

Minimal tool to scrape a web page and summarize its content using Groq's API (Gemini model).

## Setup

1. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

2. Get a Groq API key from [console.groq.com](https://console.groq.com) and set it as an environment variable:

   ```bash
   export GROQ_API_KEY="your-api-key-here"
   ```

## Usage

### Scrape a URL

```bash
python scraper.py <url>
```

This will create a JSON file (e.g., `example.com.json`) containing the page title, extracted text, and metadata.

### Summarize the scraped content

```bash
python summarizer.py <output>.json
```

This will read the JSON file, send the text to Groq's Gemini model, and save a summary to `<output>_summary.json`.

### Full pipeline

```bash
python scraper.py https://example.com && python summarizer.py example.com.json
```

## Notes

- The scraper uses rotating user‑agents to avoid simple blocks.
- The summarizer limits input to the first 10,000 characters.
- The default model is `gemma2-9b-it` (Gemini‑like). You can change it in `summarizer.py`.
