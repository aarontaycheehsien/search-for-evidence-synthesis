"""Compare CLEF TAR 2019's two label sets with each topic's screening pool.

CLEF 2019 distributes two sets of qrels for each test topic. The screening
task's (Task 2) labels judge only the PubMed records in the topic's pool:
the records the review's MEDLINE strategy returned when the organisers
re-ran it. The search task's (Task 1) labels list the review's included
references (content level) and included plus excluded references (abstract
level) that CLEF mapped to PMIDs. The overview says references outside the
pool were left out of both label sets (Kanoulas et al., 2019, section 2.3),
but the distributed Task 1 qrels contain some. This script counts them.

Writes case-pack/data/clef-2019/label-scope.csv, one row per test topic.

Usage:
  python case-pack/scripts/clef_label_scope.py --tar DIR
    (DIR is a checkout of CLEF-TAR/tar; the committed file was built
    from commit dbc13d0)
"""

import argparse
import csv
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from clef import read_qrels, read_topic  # noqa: E402
from common import DATA  # noqa: E402

TYPES = ("DTA", "Intervention", "Prognosis", "Qualitative")


def relevant(labels):
    return {pmid for pmid, value in labels.items() if value > 0}


def scope(pool, task1, task2):
    """Count one level's labels against the pool.

    pool is a set of PMIDs; task1 and task2 are {pmid: relevance} for one
    topic at one level (abstract or content).
    """
    rel1, rel2 = relevant(task1), relevant(task2)
    return {
        "task1": len(rel1),
        "task1_outside_pool": len(rel1 - pool),
        "task2": len(rel2),
        "task2_not_in_task1": len(rel2 - rel1),
    }


def qrels_file(tar, task, kind, level):
    folder = tar / "2019-TAR" / task / "Testing" / kind / "qrels"
    matches = sorted(p for p in folder.glob("*") if level in p.name)
    if len(matches) != 1:
        raise SystemExit(f"expected one {level} qrels file in {folder}, found {len(matches)}")
    return matches[0]


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--tar", type=Path, required=True, help="checkout of CLEF-TAR/tar")
    parser.add_argument("--out", type=Path, default=DATA / "clef-2019" / "label-scope.csv")
    args = parser.parse_args(argv)

    rows = []
    for kind in TYPES:
        labels = {
            (task, level): read_qrels(qrels_file(args.tar, task, kind, level))
            for task in ("Task1", "Task2")
            for level in ("abs", "content")
        }
        topics_dir = args.tar / "2019-TAR" / "Task2" / "Testing" / kind / "topics"
        for topic_file in sorted(topics_dir.iterdir()):
            topic = topic_file.name
            pool = set(read_topic(topic_file)["pmids"])
            row = {"type": kind, "topic": topic, "pool": len(pool)}
            for level in ("abs", "content"):
                counts = scope(pool, labels[("Task1", level)].get(topic, {}), labels[("Task2", level)].get(topic, {}))
                row.update({f"{level}_{key}": value for key, value in counts.items()})
            rows.append(row)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    with_outside = sum(1 for r in rows if r["content_task1_outside_pool"])
    print(f"{len(rows)} topics; {with_outside} have included references in the Task 1 labels that the pool lacks")
    print("content-level Task 1 labels:", sum(r["content_task1"] for r in rows),
          "outside pool:", sum(r["content_task1_outside_pool"] for r in rows))


if __name__ == "__main__":
    main()
