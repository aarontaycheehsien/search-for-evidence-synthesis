"""Turn ASReview simulation projects into screening logs and summary metrics.

Each log lists records in the order screened, with the label the simulation
used (title-and-abstract) and the full-text label. A simulation stops once
every relevant record has been found, so records after that point are not
in the log; all of them are irrelevant at both stages.

Usage:
  python case-pack/scripts/screening_logs.py --pool case-pack/cache/moran-2021/pool.csv \
      --out case-pack/data/moran-2021/screening RUN.asreview [RUN.asreview ...]

With --compact, each log keeps only the prior records and the records
relevant at title and abstract; every rank not listed is irrelevant at both
stages. With --aggregate, runs named NAME_sSEED are grouped by NAME and
summarised across seeds in aggregate.json.

Reads only the standard library, so it runs without ASReview installed.
"""

import argparse
import csv
import json
import re
import sqlite3
import statistics
import sys
import tempfile
import zipfile
from pathlib import Path

PRIOR_RECORDS = 2
STREAKS = (50, 100, 200)
FIXED_EFFORT = 0.20
RECALL_TARGETS = (0.8, 0.9, 0.95, 1.0)
EFFORT_POINTS = (0.1, 0.2, 0.3)


def read_order(project_path):
    """Return dataset rows in the order the simulation labelled them."""
    with tempfile.TemporaryDirectory() as tmp:
        with zipfile.ZipFile(project_path) as archive:
            archive.extract("results.db", tmp)
        connection = sqlite3.connect(Path(tmp) / "results.db")
        try:
            rows = connection.execute(
                "SELECT record.dataset_row FROM results "
                "JOIN record ON record.record_id = results.record_id "
                "ORDER BY results.rowid"
            ).fetchall()
            settings = connection.execute(
                "SELECT DISTINCT feature_extractor, classifier, querier, balancer "
                "FROM results WHERE classifier IS NOT NULL"
            ).fetchall()
        finally:
            connection.close()
    return [row[0] for row in rows], settings


def screened_to_reach(labels, total, target):
    """Records screened when found/total first reaches target, else None."""
    needed = target * total
    found = 0
    for position, label in enumerate(labels, start=1):
        found += label
        if found >= needed - 1e-9:
            return position
    return None


def recall_at(labels, total, screened):
    return round(sum(labels[:screened]) / total, 4) if total else None


def consecutive_stop(labels, run_length, pool_size, priors=PRIOR_RECORDS):
    """Position at which run_length irrelevant records in a row have been seen.

    Counting starts after the prior records. If the log ends first, the
    remaining unlabelled records are all irrelevant, so the stop falls
    run_length minus the current streak records later, capped at the pool.
    """
    streak = 0
    for position, label in enumerate(labels, start=1):
        if position <= priors:
            continue
        streak = 0 if label else streak + 1
        if streak == run_length:
            return position
    return min(len(labels) + (run_length - streak), pool_size)


def summarise(name, settings, ta, ft, pool_size, priors=PRIOR_RECORDS):
    total_ta, total_ft = sum(ta), sum(ft)
    summary = {
        "run": name,
        "model": [dict(zip(("feature_extractor", "classifier", "querier", "balancer"), s)) for s in settings],
        "pool_size": pool_size,
        "relevant_title_abstract": total_ta,
        "relevant_full_text": total_ft,
        "records_in_log": len(ta),
        "screened_to_reach_title_abstract_recall": {
            str(t): screened_to_reach(ta, total_ta, t) for t in RECALL_TARGETS
        },
        "screened_to_reach_full_text_recall": {
            str(t): screened_to_reach(ft, total_ft, t) for t in RECALL_TARGETS
        },
        "recall_at_effort": {
            str(e): {
                "screened": round(e * pool_size),
                "title_abstract": recall_at(ta, total_ta, round(e * pool_size)),
                "full_text": recall_at(ft, total_ft, round(e * pool_size)),
            }
            for e in EFFORT_POINTS
        },
        "stopping": {},
    }
    n95 = summary["screened_to_reach_title_abstract_recall"]["0.95"]
    summary["wss_at_95_title_abstract"] = round(0.95 - n95 / pool_size, 4) if n95 else None
    stops = [(f"{n}_consecutive_irrelevant", consecutive_stop(ta, n, pool_size, priors)) for n in STREAKS]
    stops.append((f"fixed_{int(FIXED_EFFORT * 100)}_percent", round(FIXED_EFFORT * pool_size)))
    for label, stop in stops:
        summary["stopping"][label] = {
            "screened": stop,
            "title_abstract_recall": recall_at(ta, total_ta, stop),
            "full_text_recall": recall_at(ft, total_ft, stop),
            "full_text_inclusions_unseen": total_ft - sum(ft[:stop]),
        }
    return summary


AGGREGATE_METRICS = {
    "wss_at_95_title_abstract": lambda s: s["wss_at_95_title_abstract"],
    "screened_to_95pc_title_abstract": lambda s: s["screened_to_reach_title_abstract_recall"]["0.95"],
    "screened_to_all_full_text": lambda s: s["screened_to_reach_full_text_recall"]["1.0"],
    "full_text_recall_at_20pc": lambda s: s["recall_at_effort"]["0.2"]["full_text"],
    **{
        f"stop_{n}_screened": (lambda n: lambda s: s["stopping"][f"{n}_consecutive_irrelevant"]["screened"])(n)
        for n in STREAKS
    },
    **{
        f"stop_{n}_full_text_unseen": (lambda n: lambda s: s["stopping"][f"{n}_consecutive_irrelevant"]["full_text_inclusions_unseen"])(n)
        for n in STREAKS
    },
}


def aggregate(summaries):
    """Group runs named NAME_sSEED by NAME; report min, median and max."""
    groups = {}
    for s in summaries:
        groups.setdefault(re.sub(r"_s\d+$", "", s["run"]), []).append(s)
    result = {}
    for name, runs in sorted(groups.items()):
        result[name] = {"runs": len(runs)}
        for metric, get in AGGREGATE_METRICS.items():
            values = [get(r) for r in runs]
            result[name][metric] = {"min": min(values), "median": statistics.median(values), "max": max(values)}
    return result


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--pool", type=Path, required=True, help="pool.csv from build_moran_pool.py")
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--compact", action="store_true", help="keep only prior and relevant records")
    parser.add_argument("--aggregate", action="store_true", help="summarise runs across seeds")
    parser.add_argument("projects", nargs="+", type=Path)
    args = parser.parse_args(argv)

    csv.field_size_limit(sys.maxsize)
    with open(args.pool, encoding="utf-8") as handle:
        pool = list(csv.DictReader(handle))
    pool_size = len(pool)
    total_ft = sum(int(r["label_ft"]) for r in pool)
    args.out.mkdir(parents=True, exist_ok=True)

    summaries = []
    for project in args.projects:
        name = project.stem
        order, settings = read_order(project)
        ta = [int(pool[i]["label_ta"]) for i in order]
        ft = [int(pool[i]["label_ft"]) for i in order]
        if sum(ft) != total_ft:
            raise SystemExit(f"{name}: log ends before every full-text inclusion was seen")
        with open(args.out / f"{name}.csv", "w", newline="", encoding="utf-8") as handle:
            writer = csv.writer(handle)
            writer.writerow(["rank", "id", "prior", "label_title_abstract", "label_full_text"])
            for rank, (row, a, b) in enumerate(zip(order, ta, ft), start=1):
                if args.compact and not (a or rank <= PRIOR_RECORDS):
                    continue
                writer.writerow([rank, pool[row]["id"], int(rank <= PRIOR_RECORDS), a, b])
        summaries.append(summarise(name, settings, ta, ft, pool_size))

    (args.out / "summary.json").write_text(json.dumps(summaries, indent=2) + "\n", encoding="utf-8")
    if args.aggregate:
        (args.out / "aggregate.json").write_text(json.dumps(aggregate(summaries), indent=2) + "\n", encoding="utf-8")
    for s in summaries:
        print(s["run"], "WSS@95 =", s["wss_at_95_title_abstract"], "stops:", json.dumps(s["stopping"]))


if __name__ == "__main__":
    main()
