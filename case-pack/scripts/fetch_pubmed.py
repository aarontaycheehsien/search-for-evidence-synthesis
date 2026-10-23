"""Fetch PubMed records into the case-pack cache.

Uses NCBI E-utilities efetch in batches and keeps the fields the exercises
need, including Date Completed (Ovid's Entry Date) for the date-limit case.
Abstracts may be under publisher copyright, so output goes to the ignored
cache, never to Git.

The output, cache/pubmed/NAME.json, has the same layout and field names as
cache/pubmed/records.json, which indexing_checks.py and analyser_checks.py
read. To fetch the included reports from NCBI and run those scripts on them:

  python case-pack/scripts/fetch_pubmed.py --reference-sets case-pack/reference-sets/*.csv --name records-ncbi
  python case-pack/scripts/indexing_checks.py --records case-pack/cache/pubmed/records-ncbi.json

Other usage:
  python case-pack/scripts/fetch_pubmed.py --pmids FILE --name NAME
  python case-pack/scripts/fetch_pubmed.py --clef-topic TOPIC_FILE --name NAME

Set NCBI_API_KEY and NCBI_EMAIL in the environment if you have them; NCBI
allows 3 requests a second without a key and 10 with one.
"""

import argparse
import csv
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
        abbreviation = art.findtext("Journal/ISOAbbreviation", "").strip()
        pub_date = art.find("Journal/JournalIssue/PubDate")
        year = ""
        if pub_date is not None:
            year = (pub_date.findtext("Year") or pub_date.findtext("MedlineDate") or "").strip()[:4]
        # Field names match cache/pubmed/records.json, which the indexing scripts read.
        records.append(
            {
                "pmid": citation.findtext("PMID", "").strip(),
                "title": _text(art.find("ArticleTitle")),
                "abstract": abstract,
                "mesh_terms": [_text(m) for m in citation.findall("MeshHeadingList/MeshHeading/DescriptorName")],
                "article_types": [_text(p) for p in art.findall("PublicationTypeList/PublicationType")],
                "year": year,
                "journal": art.findtext("Journal/Title", "").strip() or abbreviation,
                "journal_abbreviation": abbreviation,
                "language": art.findtext("Language", "").strip(),
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


def reference_set_pmids(paths):
    """PMIDs from reference-set CSV files, in order, without duplicates."""
    pmids = []
    for path in paths:
        with open(path, newline="", encoding="utf-8") as handle:
            for row in csv.DictReader(handle):
                pmid = (row.get("pmid") or "").strip()
                if pmid.isdigit() and pmid not in pmids:
                    pmids.append(pmid)
    return pmids


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
    source.add_argument("--reference-sets", type=Path, nargs="+", help="reference-set CSV files with a pmid column")
    parser.add_argument("--name", required=True, help="output name, e.g. CD010558 or records-ncbi")
    args = parser.parse_args(argv)

    if args.pmids:
        pmids = [line.strip() for line in args.pmids.read_text().splitlines() if line.strip().isdigit()]
    elif args.reference_sets:
        pmids = reference_set_pmids(args.reference_sets)
    else:
        pmids = read_topic(args.clef_topic)["pmids"]
    pause = 0.11 if os.environ.get("NCBI_API_KEY") else 0.34

    try:
        records = fetch(pmids, pause)
    except OSError as error:
        raise SystemExit(f"Could not reach NCBI E-utilities ({error}). Check network access to eutils.ncbi.nlm.nih.gov.")
    out_dir = CACHE / "pubmed"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / f"{args.name}.json", "w", encoding="utf-8") as handle:
        json.dump(
            {"fetched_on": today(), "source": f"NCBI E-utilities efetch ({EFETCH})", "records": records},
            handle,
            ensure_ascii=False,
            indent=1,
        )

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
