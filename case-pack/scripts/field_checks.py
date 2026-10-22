"""How much of the Moran search depended on fields beyond title and abstract?

The Moran et al. (2021) strategy ran in Web of Science (TS=, which also
searches author keywords and Keywords Plus) and Scopus (TITLE-ABS-KEY, which
also searches author keywords and index terms). This script applies the
strategy's three blocks to the title and abstract alone, as a translation to
a title-and-abstract field (Ovid .ti,ab. or PubMed [tiab]) would, and counts
the included records that would no longer match.

Emulation: words are lower-cased runs of letters and digits; * matches any
run of characters, including a leading *; quoted phrases are consecutive
words; W/n and NEAR/n allow up to n words between the two sides, in either
order (claims register: scopus-proximity, wos-near). Scopus's loose-phrase
handling and lemmatisation are not emulated beyond what the wildcards cover.
The titles and abstracts are those in the case pack's pool (from SYNERGY and
OpenAlex), which can differ from the text Web of Science and Scopus hold, so
a record that fails here may have matched the databases' own abstract.

With --source-dir pointing at a local clone of the authors' repository
(NPMoran/metah06_condition-dependence-of-boldness_OSF), the check is also run
on each database's own title and abstract, from the authors' initial Web of
Science and Scopus exports (wos1-6.bib, scopus1-5.bib), matched by DOI or
exact title. A record that fails on every database's own text can only have
been admitted through a field beyond title and abstract. Records added by the
update searches are not in these exports.

Reads case-pack/cache/moran-2021/pool.csv (rebuilt by build_moran_pool.py).
Writes case-pack/data/moran-2021/fields/ti-ab-only.csv and summary.md:
identifiers and flags only.

Usage:
  python case-pack/scripts/field_checks.py [--source-dir PATH]
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CACHE, DATA  # noqa: E402
from indexing_checks import Adj, Any, Terms, words  # noqa: E402
from moran_sources import clean_doi, norm_title, parse_bib  # noqa: E402


def within(left, right, n):
    """W/n or NEAR/n: up to n words between, so n + 1 word positions apart."""
    return Adj(left, right, n + 1)


CONDITION = Any(
    Terms("*nutrition*", "*nourish*", "calori*", "hunger", "starv*",
          "bod* state*", "bod* condition*", "condition depend*", "state depend*",
          "asset protection", "residual reproductive value"),
    within(Terms("diet*", "food"),
           Terms("quality", "restrict*", "depriv*", "enrich*", "availab*", "manipul*", "limit*"), 10),
)
RISK = Terms("bold*", "explorat*", "risk*", "novel*", "predat*", "refuge", "neophobi*", "neophil*")
BEHAVIOUR = Any(
    Terms("personalit*", "temperament*", "coping style*", "behavio* type*", "behavio* strateg*",
          "behavio* syndrome*", "risk taking behavio*", "developmental plasticity", "phenotypic plasticity"),
    within(Terms("behavio*"),
           Terms("animal*", "plasticity", "flexibil*", "trait*", "phenotyp*", "response*", "decision*"), 5),
)
BLOCKS = {"condition": CONDITION, "risk": RISK, "behaviour": BEHAVIOUR}


def check(title, abstract):
    """Return {block: matched} for one record's title and abstract."""
    tokens = words(title) + ["|"] + words(abstract)
    return {name: bool(expr.spans(tokens)) for name, expr in BLOCKS.items()}


def load_exports(source_dir, prefix, count):
    """Map DOI and normalised title to (title, abstract) from one database's exports."""
    by_key = {}
    for i in range(1, count + 1):
        text = (source_dir / f"{prefix}{i}.bib").read_text(encoding="utf-8-sig", errors="replace")
        for r in parse_bib(text):
            entry = (r.get("title", ""), r.get("abstract", ""))
            doi = clean_doi(r.get("doi"))
            if doi:
                by_key.setdefault(("doi", doi), entry)
            title = norm_title(r.get("title"))
            if title:
                by_key.setdefault(("title", title), entry)
    return by_key


def lookup(exports, doi, title):
    return exports.get(("doi", clean_doi(doi))) or exports.get(("title", norm_title(title)))


def flag(value):
    return "" if value is None else str(int(value))


def summarise(rows, label, column):
    group = [r for r in rows if r[label] == "1" and r[column] != ""]
    failed = [r for r in group if r[column] == "0"]
    return len(group), len(failed)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source-dir", type=Path)
    args = parser.parse_args(argv)
    wos = scopus = None
    if args.source_dir:
        wos = load_exports(args.source_dir, "wos", 6)
        scopus = load_exports(args.source_dir, "scopus", 5)

    pool = list(csv.DictReader((CACHE / "moran-2021" / "pool.csv").open(encoding="utf-8")))
    out = []
    for r in pool:
        flags = check(r["title"], r["abstract"])
        row = {
            "id": r["id"],
            "label_ta": r["label_ta"],
            "label_ft": r["label_ft"],
            **{k: str(int(v)) for k, v in flags.items()},
            "admitted_ti_ab": str(int(all(flags.values()))),
        }
        if args.source_dir:
            per_db = {}
            for name, exports in (("wos", wos), ("scopus", scopus)):
                found = lookup(exports, r["doi"], r["title"])
                per_db[name] = None if found is None else all(check(*found).values())
                row[f"in_{name}_export"] = str(int(found is not None))
                row[f"admitted_ti_ab_{name}"] = flag(per_db[name])
            available = [v for v in per_db.values() if v is not None]
            row["admitted_ti_ab_any_export"] = flag(any(available)) if available else ""
        out.append(row)

    out_dir = DATA / "moran-2021" / "fields"
    out_dir.mkdir(parents=True, exist_ok=True)
    with (out_dir / "ti-ab-only.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(out[0]))
        writer.writeheader()
        writer.writerows(out)

    columns = [("admitted_ti_ab", "Pool text (SYNERGY and OpenAlex)")]
    if args.source_dir:
        columns += [("admitted_ti_ab_wos", "Web of Science export text"),
                    ("admitted_ti_ab_scopus", "Scopus export text"),
                    ("admitted_ti_ab_any_export", "Either database's export text")]
    lines = [
        "# The Moran strategy on title and abstract only",
        "",
        "Generated by `case-pack/scripts/field_checks.py`. Do not edit by hand.",
        "",
        "Records that no longer match all three blocks when only the title and abstract are searched, "
        "out of those whose text is available from that source.",
        "",
        "| Text checked | Included at full text | Passed title and abstract | Whole pool |",
        "|---|---|---|---|",
    ]
    for column, name in columns:
        cells = []
        for label in ("label_ft", "label_ta", None):
            if label is None:
                group = [r for r in out if r[column] != ""]
                failed = sum(1 for r in group if r[column] == "0")
                total = len(group)
            else:
                total, failed = summarise(out, label, column)
            cells.append(f"{failed} of {total:,} ({failed / total:.0%})" if total else "none")
        lines.append(f"| {name} | " + " | ".join(cells) + " |")
    ft_fail = [r for r in out if r["label_ft"] == "1" and r["admitted_ti_ab"] == "0"]
    lines += [
        "",
        "Blocks failed by the included records that fail on pool text: "
        + ", ".join(f"{b} {sum(1 for r in ft_fail if r[b] == '0')}" for b in BLOCKS)
        + " (a record can fail more than one).",
    ]
    (out_dir / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
