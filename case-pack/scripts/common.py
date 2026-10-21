"""Shared helpers for case-pack scripts.

Third-party records are written under case-pack/cache/, which Git ignores.
Only identifiers, labels and our own derived files go under case-pack/data/.
"""

import datetime
import hashlib
import json
import re
import urllib.parse
import urllib.request
from pathlib import Path

CASE_PACK = Path(__file__).resolve().parent.parent
CACHE = CASE_PACK / "cache"
DATA = CASE_PACK / "data"

USER_AGENT = "search-for-evidence-synthesis case-pack builder"

_DOI_RE = re.compile(r"10\.\d{4,9}/\S+", re.IGNORECASE)


def normalise_doi(value):
    """Return a lower-case bare DOI, or '' if none can be found.

    Accepts bare DOIs, doi.org URLs and percent-encoded forms. Pandas writes
    missing values as 'nan', which is treated as missing.
    """
    if not value:
        return ""
    text = urllib.parse.unquote(str(value)).strip()
    if text.lower() in {"nan", "none", "null"}:
        return ""
    match = _DOI_RE.search(text)
    if not match:
        return ""
    return match.group(0).rstrip(".,;").lower()


def sha256_bytes(data):
    return hashlib.sha256(data).hexdigest()


def download(url, expected_sha256=None, timeout=120):
    """Fetch a URL and, if a checksum is given, refuse content that differs."""
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=timeout) as response:
        data = response.read()
    actual = sha256_bytes(data)
    if expected_sha256 and actual != expected_sha256:
        raise ValueError(
            f"Checksum mismatch for {url}: expected {expected_sha256}, got {actual}"
        )
    return data


def today():
    return datetime.date.today().isoformat()


def write_manifest(path, manifest):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
