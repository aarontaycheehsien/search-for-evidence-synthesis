"""Turn CLEF TAR participant runs into screening logs for one topic.

A run file is in TREC format (topic, Q0, PMID, rank, score, run name). Some
runs list a PMID more than once; only its first position is kept. Records
in the topic's pool that a run omits are appended in pool order, so every
log covers the whole pool.

Usage:
  python case-pack/scripts/clef_runs.py --topic CD010558 \
      --topic-file TOPIC --abs-qrels ABS --content-qrels CONTENT \
      --out case-pack/data/clef-2019/CD010558 NAME=RUNFILE [NAME=RUNFILE ...]
"""

import argparse
import csv
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from clef import read_qrels, read_topic  # noqa: E402
from screening_logs import summarise  # noqa: E402


def read_run(path, topic):
    order, seen = [], set()
    with open(path, encoding="utf-8", errors="replace") as handle:
        for line in handle:
            parts = line.split()
            if len(parts) >= 3 and parts[0] == topic and parts[2] not in seen:
                seen.add(parts[2])
                order.append(parts[2])
    return order


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--topic", required=True)
    parser.add_argument("--topic-file", type=Path, required=True)
    parser.add_argument("--abs-qrels", type=Path, required=True)
    parser.add_argument("--content-qrels", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("runs", nargs="+", help="NAME=PATH pairs")
    args = parser.parse_args(argv)

    pool = read_topic(args.topic_file)["pmids"]
    abs_labels = read_qrels(args.abs_qrels, args.topic).get(args.topic, {})
    content_labels = read_qrels(args.content_qrels, args.topic).get(args.topic, {})
    args.out.mkdir(parents=True, exist_ok=True)

    summaries = []
    for item in args.runs:
        name, path = item.split("=", 1)
        ranked = [p for p in read_run(path, args.topic) if p in set(pool)]
        order = ranked + [p for p in pool if p not in set(ranked)]
        ta = [abs_labels.get(p, 0) for p in order]
        ft = [content_labels.get(p, 0) for p in order]
        with open(args.out / f"{name}.csv", "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["rank", "pmid", "ranked_by_run", "label_title_abstract", "label_full_text"])
            for rank, (pmid, a, b) in enumerate(zip(order, ta, ft), start=1):
                writer.writerow([rank, pmid, int(rank <= len(ranked)), a, b])
        summary = summarise(name, [], ta, ft, len(pool), priors=0)
        summary["records_ranked_by_run"] = len(ranked)
        summary["source_file"] = Path(path).name
        summaries.append(summary)

    (args.out / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")
    for s in summaries:
        print(s["run"], "ranked", s["records_ranked_by_run"], "WSS@95 =", s["wss_at_95_title_abstract"],
              "stops:", json.dumps(s["stopping"]))


if __name__ == "__main__":
    main()
