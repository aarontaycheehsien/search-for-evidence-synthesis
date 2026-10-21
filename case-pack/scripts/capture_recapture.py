"""Estimate how many eligible records both Moran databases missed.

Two-source capture-recapture on the Moran et al. (2021) searches: Web of
Science and Scopus are the two "captures", and a record found by both is a
"recapture". The counts come from sources-and-deduplication.json (built by
moran_sources.py), matching by DOI or exact title.

Two estimators are reported:
  Lincoln-Petersen  N = n1 * n2 / m
  Chapman           N = (n1 + 1)(n2 + 1) / (m + 1) - 1
with Chapman's variance (n1 + 1)(n2 + 1)(n1 - m)(n2 - m) / ((m + 1)^2 (m + 2))
and a normal-approximation 95% interval, floored at the number found.

Both assume that the two sources find records independently and that every
record is equally likely to be found. Here both databases were searched with
the same strategy, so a record whose wording the strategy misses is likely to
be missed in both; that positive dependence makes the estimates too low.

Writes case-pack/data/stopping/capture-recapture.csv.

Usage:
  python case-pack/scripts/capture_recapture.py
"""

import csv
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA  # noqa: E402


def estimate(both, first_only, second_only):
    """Return capture-recapture estimates for two sources."""
    n1 = both + first_only
    n2 = both + second_only
    m = both
    found = both + first_only + second_only
    lincoln_petersen = n1 * n2 / m
    chapman = (n1 + 1) * (n2 + 1) / (m + 1) - 1
    variance = (n1 + 1) * (n2 + 1) * (n1 - m) * (n2 - m) / ((m + 1) ** 2 * (m + 2))
    half_width = 1.96 * math.sqrt(variance)
    return {
        "first_source": n1,
        "second_source": n2,
        "both": m,
        "found": found,
        "lincoln_petersen": round(lincoln_petersen, 1),
        "chapman": round(chapman, 1),
        "chapman_low": round(max(found, chapman - half_width), 1),
        "chapman_high": round(chapman + half_width, 1),
        "estimated_missed": round(chapman - found, 1),
    }


def main():
    sources = json.loads((DATA / "moran-2021" / "sources-and-deduplication.json").read_text(encoding="utf-8"))
    rows = []
    for stage, key in (("full text", "full_text_included"), ("title and abstract", "title_abstract_included")):
        counts = sources["eligible_by_database"][key]
        row = {"stage": stage}
        row.update(estimate(counts["both"], counts["wos_only"], counts["scopus_only"]))
        rows.append(row)
        print(row)
    out_dir = DATA / "stopping"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "capture-recapture.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


if __name__ == "__main__":
    main()
