"""Build the Moran et al. (2021) teaching pool.

Joins two sources by DOI:

- the authors' deduplicated screening export (titles and abstracts), from
  their GitHub repository at a pinned commit; and
- the title-and-abstract and full-text labels in SYNERGY's
  Moran_2021_corrected variant, at a pinned commit.

SYNERGY version 1's Moran_2021 labels are not used: almost none of the
records it labels as included were included by the review. See
docs/case-pack.md.

Outputs:
  case-pack/cache/moran-2021/pool.csv      text and labels (not committed)
  case-pack/data/moran-2021/labels.csv     identifiers and labels (committed)
  case-pack/data/moran-2021/manifest.json  sources, checksums and counts

Usage:
  python case-pack/scripts/build_moran_pool.py
  python case-pack/scripts/build_moran_pool.py --source-dir DIR
    (DIR holds pool.csv and corrected.csv already downloaded)
"""

import argparse
import csv
import io
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CACHE, DATA, download, normalise_doi, sha256_bytes, today, write_manifest  # noqa: E402

SOURCES = {
    "pool": {
        "url": "https://raw.githubusercontent.com/NPMoran/metah06_condition-dependence-of-boldness_OSF/"
        "b25a3c22e2da63cd2fa9e92d05d7991ae0e8564f/screening_ref_data_rayyan.csv",
        "sha256": "d0a8832b7aa336e37764f31292514b9165e57aa6ababff4f92a1f0bb8a1fa92d",
        "description": "Authors' deduplicated screening export (Rayyan), titles and abstracts",
    },
    "corrected": {
        "url": "https://raw.githubusercontent.com/asreview/synergy-dataset/"
        "dc2dadfdbb98eb1b4259604789abd640aa3b693e/datasets/Moran_2021_corrected/Moran_2021_corrected_ids.csv",
        "sha256": "6a653603917705a9f8f703e3a91708e21f0424274b780cf7346a162374de8fb9",
        "description": "SYNERGY Moran_2021_corrected labels (CC0); not part of the version 1 release",
    },
}


def read_csv_bytes(data):
    csv.field_size_limit(sys.maxsize)
    return list(csv.DictReader(io.StringIO(data.decode("utf-8", errors="replace"))))


def build(pool_rows, label_rows):
    """Join labels to text by DOI.

    Returns (records, stats). A DOI that appears more than once in the label
    file keeps the highest label at each stage; a DOI that appears more than
    once in the text file keeps the first text.
    """
    labels = {}
    for row in label_rows:
        doi = normalise_doi(row.get("doi"))
        if not doi:
            continue
        ta = int(row.get("label_abstract_included") or 0)
        ft = int(row.get("label_included") or 0)
        old = labels.get(doi, (0, 0))
        labels[doi] = (max(old[0], ta), max(old[1], ft))

    text = {}
    for row in pool_rows:
        doi = normalise_doi(row.get("url"))
        if doi and doi not in text:
            text[doi] = row

    records = []
    for doi, (ta, ft) in sorted(labels.items()):
        source = text.get(doi)
        if source is None:
            continue
        records.append(
            {
                "id": f"doi:{doi}",
                "doi": doi,
                "title": (source.get("title") or "").strip(),
                "abstract": (source.get("abstract") or "").strip(),
                "year": (source.get("year") or "").strip(),
                "label_ta": ta,
                "label_ft": ft,
            }
        )

    stats = {
        "label_rows": len(label_rows),
        "label_rows_with_doi": sum(1 for r in label_rows if normalise_doi(r.get("doi"))),
        "distinct_label_dois": len(labels),
        "text_rows": len(pool_rows),
        "joined_records": len(records),
        "ta_included_in_labels": sum(1 for v in labels.values() if v[0]),
        "ta_included_joined": sum(r["label_ta"] for r in records),
        "ft_included_in_labels": sum(1 for v in labels.values() if v[1]),
        "ft_included_joined": sum(r["label_ft"] for r in records),
        "ft_without_ta": sum(1 for r in records if r["label_ft"] and not r["label_ta"]),
    }
    return records, stats


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--source-dir", type=Path, help="use pool.csv and corrected.csv from this directory")
    args = parser.parse_args(argv)

    raw = {}
    for key, source in SOURCES.items():
        if args.source_dir:
            data = (args.source_dir / f"{key}.csv").read_bytes()
            if sha256_bytes(data) != source["sha256"]:
                raise SystemExit(f"{key}.csv does not match the pinned checksum")
        else:
            data = download(source["url"], source["sha256"])
        raw[key] = data

    records, stats = build(read_csv_bytes(raw["pool"]), read_csv_bytes(raw["corrected"]))

    cache_dir = CACHE / "moran-2021"
    cache_dir.mkdir(parents=True, exist_ok=True)
    with open(cache_dir / "pool.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(records[0]))
        writer.writeheader()
        writer.writerows(records)

    data_dir = DATA / "moran-2021"
    data_dir.mkdir(parents=True, exist_ok=True)
    with open(data_dir / "labels.csv", "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "doi", "label_ta", "label_ft"])
        writer.writeheader()
        for record in records:
            writer.writerow({k: record[k] for k in ("id", "doi", "label_ta", "label_ft")})

    write_manifest(
        data_dir / "manifest.json",
        {
            "built_on": today(),
            "script": "case-pack/scripts/build_moran_pool.py",
            "sources": SOURCES,
            "join": "normalised DOI; records without a DOI in either source are dropped",
            "counts": stats,
        },
    )
    for key, value in stats.items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
