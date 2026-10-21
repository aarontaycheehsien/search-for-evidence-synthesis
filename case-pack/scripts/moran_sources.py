"""Deduplication and database-contribution analysis for Moran et al. (2021).

Reads the authors' initial Web of Science (wos1-6.bib) and Scopus
(scopus1-5.bib) exports from a local clone of their repository, compares
deduplication rules, and counts which database contributed each eligible
study. The exports contain Web of Science and Scopus records, so they are
read from the clone and never copied; only counts are written.

Usage:
  git clone https://github.com/NPMoran/metah06_condition-dependence-of-boldness_OSF SRC
  git -C SRC checkout b25a3c22e2da63cd2fa9e92d05d7991ae0e8564f
  python case-pack/scripts/moran_sources.py --source-dir SRC
"""

import argparse
import csv
import difflib
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import DATA, normalise_doi, today  # noqa: E402

FIELD = re.compile(r"^\s*(\w[\w-]*)\s*=\s*\{(.*)\}\s*,?\s*$", re.DOTALL)


def parse_bib(text):
    """Minimal BibTeX reader for these exports: returns a list of field dicts."""
    entries = []
    for chunk in re.split(r"\n\s*@", "\n" + text)[1:]:
        body = chunk.split("{", 1)[1] if "{" in chunk else ""
        fields, current = {}, ""
        for line in body.splitlines()[1:]:
            current = f"{current} {line.strip()}" if current else line.strip()
            match = FIELD.match(current)
            if match and current.count("{") == current.count("}"):
                fields[match.group(1).lower()] = match.group(2).strip("{} ")
                current = ""
        entries.append(fields)
    return entries


def norm_title(title):
    return re.sub(r"[^a-z0-9]", "", (title or "").lower())


def load(source_dir, prefix, count):
    records = []
    for i in range(1, count + 1):
        text = (source_dir / f"{prefix}{i}.bib").read_text(encoding="utf-8-sig", errors="replace")
        records.extend(parse_bib(text))
    return [
        {
            "doi": normalise_doi(r.get("doi")),
            "doi_clean": clean_doi(r.get("doi")),
            "title": norm_title(r.get("title")),
            "year": (r.get("year") or "")[:4],
        }
        for r in records
    ]


def clean_doi(value):
    """DOI with BibTeX brace escapes removed (Web of Science writes [ as {[})
    and a doubled slash after the prefix collapsed."""
    doi = normalise_doi((value or "").replace("{", "").replace("}", ""))
    return re.sub(r"^(10\.\d+)//", r"\1/", doi)


def cluster(records, use_doi, use_title, fuzzy=None, doi_key="doi"):
    """Union-find clustering. Returns a list of cluster ids, one per record."""
    parent = list(range(len(records)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    def union(a, b):
        parent[find(a)] = find(b)

    for key, enabled in ((doi_key, use_doi), ("title", use_title)):
        if not enabled:
            continue
        seen = {}
        for i, r in enumerate(records):
            value = r[key]
            if value:
                if value in seen:
                    union(i, seen[value])
                else:
                    seen[value] = i
    if fuzzy:
        blocks = {}
        for i, r in enumerate(records):
            if r["title"]:
                blocks.setdefault(r["title"][:12], []).append(i)
        for members in blocks.values():
            for x in range(len(members)):
                for y in range(x + 1, len(members)):
                    a, b = records[members[x]]["title"], records[members[y]]["title"]
                    if difflib.SequenceMatcher(None, a, b).ratio() >= fuzzy:
                        union(members[x], members[y])
    return [find(i) for i in range(len(records))]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source-dir", type=Path, required=True)
    args = parser.parse_args(argv)

    wos = load(args.source_dir, "wos", 6)
    scopus = load(args.source_dir, "scopus", 5)
    for r in wos:
        r["db"] = "wos"
    for r in scopus:
        r["db"] = "scopus"
    combined = wos + scopus

    rules = {
        "doi_only": dict(use_doi=True, use_title=False),
        "doi_only_cleaned": dict(use_doi=True, use_title=False, doi_key="doi_clean"),
        "exact_title_only": dict(use_doi=False, use_title=True),
        "doi_or_exact_title": dict(use_doi=True, use_title=True),
        "doi_or_title_similarity_0.95": dict(use_doi=True, use_title=True, fuzzy=0.95),
        "doi_or_title_similarity_0.90": dict(use_doi=True, use_title=True, fuzzy=0.90),
    }
    dedup = {name: len(set(cluster(combined, **rule))) for name, rule in rules.items()}

    # Database contribution, using DOI or exact title.
    ids = cluster(combined, use_doi=True, use_title=True)
    databases = {}
    for record, cid in zip(combined, ids):
        databases.setdefault(cid, set()).add(record["db"])
    doi_to_cluster = {r["doi"]: cid for r, cid in zip(combined, ids) if r["doi"]}

    with open(DATA / "moran-2021" / "labels.csv", encoding="utf-8") as handle:
        labels = list(csv.DictReader(handle))

    def contribution(stage):
        counts = {"both": 0, "wos_only": 0, "scopus_only": 0, "not_matched": 0}
        for row in labels:
            if row[stage] != "1":
                continue
            cid = doi_to_cluster.get(row["doi"])
            if cid is None:
                counts["not_matched"] += 1
            else:
                dbs = databases[cid]
                counts["both" if len(dbs) == 2 else f"{next(iter(dbs))}_only"] += 1
        return counts

    clusters = list(databases.values())
    result = {
        "built_on": today(),
        "script": "case-pack/scripts/moran_sources.py",
        "source": "NPMoran/metah06_condition-dependence-of-boldness_OSF@b25a3c22e2da63cd2fa9e92d05d7991ae0e8564f, wos1-6.bib and scopus1-5.bib",
        "records": {"web_of_science": len(wos), "scopus": len(scopus), "combined": len(combined)},
        "records_with_doi": {"web_of_science": sum(1 for r in wos if r["doi"]), "scopus": sum(1 for r in scopus if r["doi"])},
        "reported": {"authors_revtools_deduplicated": 5509, "article_screened_title_abstract": 5453},
        "deduplicated_counts": dedup,
        "unique_records_by_database_doi_or_exact_title": {
            "both": sum(1 for d in clusters if len(d) == 2),
            "web_of_science_only": sum(1 for d in clusters if d == {"wos"}),
            "scopus_only": sum(1 for d in clusters if d == {"scopus"}),
        },
        "eligible_by_database": {
            "title_abstract_included": contribution("label_ta"),
            "full_text_included": contribution("label_ft"),
        },
    }
    out = DATA / "moran-2021" / "sources-and-deduplication.json"
    out.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
