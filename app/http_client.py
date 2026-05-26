"""
SE — HTTP: outbound request/response handling via the standard library (urllib).
"""

import json
import logging
import urllib.error
import urllib.request

from app.exceptions import NetworkError

logger = logging.getLogger(__name__)


def fetch_json(url: str, timeout: float = 3.0) -> dict:
    """
    Perform an HTTP GET and parse JSON (used by the health servlet for demonstration).
    """
    request = urllib.request.Request(
        url,
        headers={"User-Agent": "TasteMap/1.0", "Accept": "application/json"},
        method="GET",
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            charset = response.headers.get_content_charset() or "utf-8"
            body = response.read().decode(charset)
            return json.loads(body) if body.strip() else {}
    except urllib.error.URLError as exc:
        logger.warning("HTTP fetch failed for %s: %s", url, exc)
        raise NetworkError(f"HTTP request failed: {exc}") from exc
    except json.JSONDecodeError as exc:
        raise NetworkError("HTTP response was not valid JSON.") from exc
