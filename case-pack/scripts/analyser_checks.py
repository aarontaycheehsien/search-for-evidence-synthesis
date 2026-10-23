"""Test how analyser choices change what CD010558's condition block admits.

Uses the emulation in indexing_checks.py on the cached PubMed records of
CD010558's included studies, and writes one row per record:

- lines_admitting: which of lines 1 to 6 (the condition block) admit it;
- line4_min_gap: the smallest word gap between depress* and line 4's
  second group (refractor*, resistan*, chronic*, persist*) in the title or
  abstract, where 1 means adjacent; blank if they never co-occur;
- the same lines under a hypothetical analyser that keeps hyphenated words
  as single tokens ("treatment-resistant" stays one word).

The hyphen variant is a thought experiment about analysers in general, not
a description of any platform.

Usage:
  python case-pack/scripts/analyser_checks.py [--records FILE]
"""

import csv
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import indexing_checks as ic  # noqa: E402

LINE4_LEFT = ic.Terms("depress*")
LINE4_RIGHT = ic.Terms("refractor*", "resistan*", "chronic*", "persist*")


def hyphen_kept(text):
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", (text or "").lower())


def lines_admitting(record):
    lines = ic.cd010558_lines(record)
    return [i for i in range(1, 7) if lines[i]]


def min_gap(record):
    best = None
    for field in ("ti", "ab"):
        for tokens in record.fields[field]:
            for a in LINE4_LEFT.spans(tokens):
                for b in LINE4_RIGHT.spans(tokens):
                    if b[0] > a[1]:
                        gap = b[0] - a[1]
                    elif a[0] > b[1]:
                        gap = a[0] - b[1]
                    else:
                        continue
                    best = gap if best is None else min(best, gap)
    return best


def main(argv=None):
    records = ic.load_records(ic.records_argument(argv, "Analyser choices on CD010558's condition block."))
    rows = []
    for ref in ic.reference_rows("CD010558"):
        data = records[ref["pmid"]]
        default = ic.Record(data)
        row = {
            "pmid": ref["pmid"],
            "study_id": ref["study_id"],
            "in_clef_pool": ref["in_clef_pool"],
            "lines_admitting": ";".join(map(str, lines_admitting(default))),
            "line4_min_gap": "" if min_gap(default) is None else min_gap(default),
        }
        original = ic.words
        ic.words = hyphen_kept
        try:
            row["lines_admitting_hyphen_kept"] = ";".join(map(str, lines_admitting(ic.Record(data))))
        finally:
            ic.words = original
        rows.append(row)

    out = ic.DATA / "indexing" / "CD010558-analyser.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    only4 = [r["study_id"] for r in rows if r["lines_admitting"] == "4"]
    lost = [r["study_id"] for r in rows if r["lines_admitting"] and not r["lines_admitting_hyphen_kept"]]
    print("records admitted only by line 4:", only4)
    print("records the condition block loses if hyphenated words stay whole:", lost)


if __name__ == "__main__":
    main()
