"""Fetch PubMed records into the case-pack cache.

Uses NCBI E-utilities efetch in batches and keeps the fields the exercises
need, including Date Completed (Ovid's Entry Date) for the date-limit case.
Abstracts may be under publisher copyright, so output goes to the ignored
cache, never to Git.

Usage:
  python case-pack/scripts/fetch_pubmed.py --pmids FILE --name NAME
  python case-pack/scripts/fetch_pubmed.py --clef-topic TOPIC_FILE --name NAME

Set NCBI_API_KEY and NCBI_EMAIL in the environment if you have them; NCBI
allows 3 requests a second without a key and 10 with one.
"""

import argparse
import json
import os
import sys
import time
import urllib.parse
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from clef import read_topic  # noqa: E402
from common import CACHE, download, today, write_manifest  # noqa: E402

EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
BATCH = 200


def _date(element):
    if element is None:
        return ""
    parts = [element.findtext(tag) for tag in ("Year", "Month", "Day")]
    return "-".join(p for p in parts if p)


def _text(element):
    return "".join(element.itertext()).strip() if element is not None else ""


def parse_efetch(xml_bytes):
    """Parse an efetch PubmedArticleSet into a list of dicts."""
    root = ET.fromstring(xml_bytes)
    records = []
    for article in root.iter("PubmedArticle"):
        citation = article.find("MedlineCitation")
        art = citation.find("Article")
        abstract = " ".join(
            _text(part) for part in art.findall("Abstract/AbstractText")
        ).strip()
        history = {
            d.get("PubStatus"): _date(d)
            for d in article.findall("PubmedData/History/PubMedPubDate")
        }
        records.append(
            {
                "pmid": citation.findtext("PMID", "").strip(),
                "title": _text(art.find("ArticleTitle")),
                "abstract": abstract,
                "journal": art.findtext("Journal/ISOAbbreviation", "").strip(),
                "publication_types": [_text(p) for p in art.findall("PublicationTypeList/PublicationType")],
                "mesh_headings": [_text(m) for m in citation.findall("MeshHeadingList/MeshHeading/DescriptorName")],
                "indexing_method": citation.get("IndexingMethod", ""),
                "status": citation.get("Status", ""),
                "date_completed": _date(citation.find("DateCompleted")),
                "date_revised": _date(citation.find("DateRevised")),
                "entrez_date": history.get("entrez", ""),
                "doi": next(
                    (_text(i) for i in article.findall("PubmedData/ArticleIdList/ArticleId") if i.get("IdType") == "doi"),
                    "",
                ),
            }
        )
    return records


def fetch(pmids, pause):
    params = {"db": "pubmed", "retmode": "xml", "tool": "search-for-evidence-synthesis"}
    if os.environ.get("NCBI_API_KEY"):
        params["api_key"] = os.environ["NCBI_API_KEY"]
    if os.environ.get("NCBI_EMAIL"):
        params["email"] = os.environ["NCBI_EMAIL"]
    records = []
    for start in range(0, len(pmids), BATCH):
        batch = pmids[start:start + BATCH]
        url = EFETCH + "?" + urllib.parse.urlencode({**params, "id": ",".join(batch)})
        records.extend(parse_efetch(download(url)))
        time.sleep(pause)
    return records


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    source = parser.add_mutually_exclusive_group(required=True)
    source.add_argument("--pmids", type=Path, help="file with one PMID per line")
    source.add_argument("--clef-topic", type=Path, help="CLEF TAR topic file")
    parser.add_argument("--name", required=True, help="output name, e.g. CD010558")
    args = parser.parse_args(argv)

    if args.pmids:
        pmids = [line.strip() for line in args.pmids.read_text().splitlines() if line.strip().isdigit()]
    else:
        pmids = read_topic(args.clef_topic)["pmids"]
    pause = 0.11 if os.environ.get("NCBI_API_KEY") else 0.34

    try:
        records = fetch(pmids, pause)
    except OSError as error:
        raise SystemExit(f"Could not reach NCBI E-utilities ({error}). Check network access to eutils.ncbi.nlm.nih.gov.")
    out_dir = CACHE / "pubmed"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / f"{args.name}.jsonl", "w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    returned = {r["pmid"] for r in records}
    write_manifest(
        out_dir / f"{args.name}.manifest.json",
        {
            "fetched_on": today(),
            "requested": len(pmids),
            "returned": len(returned),
            "missing_pmids": sorted(set(pmids) - returned),
            "source": EFETCH,
            "note": "Records reflect PubMed on the fetch date, not when the review searched.",
        },
    )
    print(f"requested {len(pmids)}, returned {len(returned)}")


if __name__ == "__main__":
    main()
