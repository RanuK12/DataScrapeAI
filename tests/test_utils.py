"""Tests for utility functions."""

import pytest

from src.datascrapeai.utils import sanitize_filename, extract_text


class TestSanitizeFilename:
    def test_basic_url(self):
        url = "https://example.com/page"
        result = sanitize_filename(url)
        assert result == "example.com_page"

    def test_https_removed(self):
        url = "https://example.com"
        result = sanitize_filename(url)
        assert result == "example.com"

    def test_http_removed(self):
        url = "http://example.com"
        result = sanitize_filename(url)
        assert result == "example.com"

    def test_special_chars(self):
        url = "https://example.com/path?query=1&x=y"
        result = sanitize_filename(url)
        assert "?" not in result
        assert "&" not in result

    def test_max_length(self):
        url = "https://" + "a" * 100 + ".com"
        result = sanitize_filename(url)
        assert len(result) <= 50


class TestExtractText:
    def test_simple_html(self):
        html = "<html><body><p>Hello World</p></body></html>"
        text = extract_text(html)
        assert text == "Hello World"

    def test_removes_script(self):
        html = "<html><body><script>alert('x')</script><p>Visible</p></body></html>"
        text = extract_text(html)
        assert "alert" not in text
        assert "Visible" in text

    def test_removes_style(self):
        html = "<html><head><style>body{color:red}</style></head><body><p>Text</p></body></html>"
        text = extract_text(html)
        assert "color" not in text
        assert "Text" in text

    def test_multiple_lines(self):
        html = "<html><body><p>Line1</p><p>Line2</p></body></html>"
        text = extract_text(html)
        assert "Line1" in text
        assert "Line2" in text
