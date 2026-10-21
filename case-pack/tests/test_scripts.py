"""Offline tests for the case-pack scripts.

Run from the repository root:
  python -m unittest discover -s case-pack/tests
"""

import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

from analyser_checks import hyphen_kept, min_gap  # noqa: E402
from build_moran_pool import build  # noqa: E402
from clef import read_qrels, read_topic  # noqa: E402
from clef_label_scope import scope  # noqa: E402
from common import normalise_doi  # noqa: E402
from fetch_pubmed import parse_efetch  # noqa: E402
from indexing_checks import Adj, Record, Terms, cd010558_row, words  # noqa: E402
from ranking_checks import bm25_scores, expand, ranks, recall_at  # noqa: E402

FIXTURES = HERE / "fixtures"


class NormaliseDoiTest(unittest.TestCase):
    def test_forms(self):
        self.assertEqual(normalise_doi("10.1016/0741-8329(91)91168-2"), "10.1016/0741-8329(91)91168-2")
        self.assertEqual(normalise_doi("https://doi.org/10.1111/BRV.12655"), "10.1111/brv.12655")
        self.assertEqual(normalise_doi("https://doi.org/10.1002%2Fjrsm.1378"), "10.1002/jrsm.1378")
        self.assertEqual(normalise_doi("10.1234/abc."), "10.1234/abc")

    def test_missing(self):
        for value in (None, "", "nan", "https://doi.org/nan", "not a doi"):
            self.assertEqual(normalise_doi(value), "")


class ClefTest(unittest.TestCase):
    def test_topic(self):
        topic = read_topic(FIXTURES / "clef_topic_synthetic")
        self.assertEqual(topic["topic"], "SYN0001")
        self.assertEqual(len(topic["query"]), 3)
        self.assertEqual(topic["pmids"], ["900000001", "900000002", "900000003"])

    def test_qrels(self):
        path = FIXTURES / "qrels_synthetic"
        path.write_text("SYN0001 0 900000001 1\nSYN0001 0 900000002 0\nSYN0002 0 900000009 1\n")
        try:
            qrels = read_qrels(path, topic="SYN0001")
        finally:
            path.unlink()
        self.assertEqual(qrels, {"SYN0001": {"900000001": 1, "900000002": 0}})


class ClefLabelScopeTest(unittest.TestCase):
    def test_counts_labels_outside_pool(self):
        pool = {"1", "2", "3"}
        task1 = {"1": 1, "4": 1, "5": 1, "6": 0}
        task2 = {"1": 1, "2": 0, "3": 0}
        self.assertEqual(
            scope(pool, task1, task2),
            {"task1": 3, "task1_outside_pool": 2, "task2": 1, "task2_not_in_task1": 0},
        )


class IndexingChecksTest(unittest.TestCase):
    def test_wildcards_and_phrases(self):
        self.assertTrue(Terms("randomi#ed").spans(words("A randomised trial")))
        self.assertTrue(Terms("randomi#ed").spans(words("A randomized trial")))
        self.assertFalse(Terms("randomi#ed").spans(words("A randomed trial")))
        self.assertTrue(Terms("group?").spans(words("two groups")))
        self.assertFalse(Terms("group?").spans(words("grouping")))
        self.assertTrue(Terms("double-blind*").spans(words("a double blinded design")))
        self.assertTrue(Terms("interview:").spans(words("semi-structured interviews")))

    def test_adjacency_counts_words_either_order(self):
        expr = Adj(Terms("depress*"), Terms("resistan*"), 3)
        self.assertTrue(expr.spans(words("treatment resistant depression")))
        self.assertTrue(expr.spans(words("depression that was resistant")))
        self.assertFalse(expr.spans(words("depression in adults who were resistant")))

    def test_cd010558_routes(self):
        record = Record({
            "pmid": "1",
            "title": "Therapy for treatment-resistant depression: a randomised controlled trial",
            "abstract": "",
            "mesh_terms": ["Humans"],
            "article_types": ["Journal Article"],
        })
        row = cd010558_row(record)
        self.assertEqual(row["condition_heading"], False)
        self.assertEqual(row["condition_text"], True)
        self.assertEqual(row["design_publication_type"], False)
        self.assertEqual(row["design_text"], True)
        self.assertEqual(row["admitted_before_date_limit"], True)
        letter = Record({"pmid": "2", "title": "Treatment-resistant depression trial", "abstract": "",
                         "mesh_terms": [], "article_types": ["Letter"]})
        self.assertEqual(cd010558_row(letter)["removed_by_not_block"], True)

    def test_line4_gap_and_hyphen_analyser(self):
        record = Record({"pmid": "3", "title": "Treatment-resistant major depressive disorder", "abstract": "",
                         "mesh_terms": [], "article_types": []})
        self.assertEqual(min_gap(record), 2)
        self.assertEqual(hyphen_kept("Treatment-resistant major depression"), ["treatment-resistant", "major", "depression"])


class RankingChecksTest(unittest.TestCase):
    def test_expansion(self):
        vocabulary = {"nutrition", "malnutrition", "nutritional", "diet", "diets"}
        self.assertEqual(expand("diet*", vocabulary), {"diet", "diets"})
        self.assertEqual(expand("*nutrition*", vocabulary), {"nutrition", "malnutrition", "nutritional"})
        self.assertEqual(expand("hunger", vocabulary), set())

    def test_bm25_prefers_rarer_and_more_frequent_terms(self):
        docs = [["diet", "diet", "boldness"], ["diet", "other"], ["other", "words"]]
        scores = bm25_scores(docs, ["diet", "boldness"])
        self.assertGreater(scores[0], scores[1])
        self.assertEqual(scores[2], 0.0)
        self.assertEqual(ranks(scores), [1, 2, 3])
        self.assertEqual(recall_at([1, 2, 3], [0, 1, 1], 2), 0.5)


class ParseEfetchTest(unittest.TestCase):
    def setUp(self):
        self.records = parse_efetch((FIXTURES / "efetch_synthetic.xml").read_bytes())

    def test_fields(self):
        first = self.records[0]
        self.assertEqual(first["pmid"], "900000001")
        self.assertEqual(first["title"], "A synthetic trial record")
        self.assertEqual(first["abstract"], "First part. Second part.")
        self.assertEqual(first["date_completed"], "2017-06-02")
        self.assertEqual(first["entrez_date"], "2017-3-7")
        self.assertEqual(first["indexing_method"], "Automated")
        self.assertIn("Randomized Controlled Trial", first["publication_types"])
        self.assertEqual(first["mesh_headings"], ["Depressive Disorder, Treatment-Resistant"])
        self.assertEqual(first["doi"], "10.9999/synthetic.0001")

    def test_missing_parts(self):
        second = self.records[1]
        self.assertEqual(second["abstract"], "")
        self.assertEqual(second["date_completed"], "")
        self.assertEqual(second["status"], "In-Process")
        self.assertEqual(second["doi"], "")


class BuildMoranTest(unittest.TestCase):
    def test_join_and_duplicates(self):
        pool = [
            {"url": "10.9999/a", "title": "A", "abstract": "aa", "year": "2001"},
            {"url": "10.9999/a", "title": "A duplicate", "abstract": "", "year": "2001"},
            {"url": "10.9999/b", "title": "B", "abstract": "bb", "year": "2002"},
            {"url": "", "title": "No DOI", "abstract": "", "year": ""},
        ]
        labels = [
            {"doi": "https://doi.org/10.9999/a", "label_abstract_included": "1", "label_included": "0"},
            {"doi": "https://doi.org/10.9999/A", "label_abstract_included": "1", "label_included": "1"},
            {"doi": "https://doi.org/10.9999/b", "label_abstract_included": "0", "label_included": "0"},
            {"doi": "https://doi.org/10.9999/c", "label_abstract_included": "1", "label_included": "1"},
            {"doi": "https://doi.org/nan", "label_abstract_included": "0", "label_included": "0"},
        ]
        records, stats = build(pool, labels)
        self.assertEqual([r["id"] for r in records], ["doi:10.9999/a", "doi:10.9999/b"])
        self.assertEqual(records[0]["title"], "A")
        self.assertEqual((records[0]["label_ta"], records[0]["label_ft"]), (1, 1))
        self.assertEqual(stats["distinct_label_dois"], 3)
        self.assertEqual(stats["ft_included_in_labels"], 2)
        self.assertEqual(stats["ft_included_joined"], 1)


if __name__ == "__main__":
    unittest.main()


class ScreeningMetricsTest(unittest.TestCase):
    def test_reach_and_recall(self):
        from screening_logs import recall_at, screened_to_reach

        labels = [1, 0, 1, 0, 0, 1]
        self.assertEqual(screened_to_reach(labels, 3, 1.0), 6)
        self.assertEqual(screened_to_reach(labels, 3, 0.6), 3)
        self.assertEqual(recall_at(labels, 3, 3), 0.6667)

    def test_consecutive_stop(self):
        from screening_logs import consecutive_stop

        # Two prior records are not counted towards the streak.
        labels = [1, 0, 0, 0, 1, 0, 0, 0]
        self.assertEqual(consecutive_stop(labels, 3, 100), 8)
        # The log ends after the last relevant record: the stop is projected
        # into the unlabelled, all-irrelevant remainder.
        self.assertEqual(consecutive_stop([1, 0, 1, 0], 3, 100), 6)
        self.assertEqual(consecutive_stop([1, 0, 1, 0], 3, 5), 5)

    def test_aggregate_groups_by_seed_suffix(self):
        from screening_logs import aggregate, summarise

        runs = [
            summarise(f"model_s{seed}", [], labels, labels, 300, priors=0)
            for seed, labels in ((1, [1] * 3 + [0] * 7), (2, [0] * 7 + [1] * 3))
        ]
        result = aggregate(runs)
        self.assertEqual(list(result), ["model"])
        self.assertEqual(result["model"]["runs"], 2)
        self.assertEqual(result["model"]["screened_to_all_full_text"], {"min": 3, "median": 6.5, "max": 10})


class MoranSourcesTest(unittest.TestCase):
    def test_parse_bib_and_clean_doi(self):
        from moran_sources import clean_doi, parse_bib

        text = (
            "@article{ ISI:1,\nTitle = {{A Title\n   Over Two Lines}},\n"
            "DOI = {{10.1890/0012-9658(1997)078{[}1266:RFLRSO]2.0.CO;2}},\n}\n\n"
            "@ARTICLE{key2,\ntitle={Second},\ndoi={10.1037//0022-006X.70.5.1119},\n}\n"
        )
        entries = parse_bib(text)
        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[0]["title"], "A Title Over Two Lines")
        self.assertEqual(clean_doi(entries[0]["doi"]), "10.1890/0012-9658(1997)078[1266:rflrso]2.0.co;2")
        self.assertEqual(clean_doi(entries[1]["doi"]), "10.1037/0022-006x.70.5.1119")

    def test_aggregate_markdown(self):
        from screening_logs import aggregate, aggregate_markdown, summarise

        runs = [summarise(f"m_s{i}", [], [1, 0, 1, 0], [1, 0, 0, 0], 100, priors=0) for i in (1, 2)]
        table = aggregate_markdown(aggregate(runs))
        self.assertIn("| Measure | m (2 runs) |", table)
        self.assertIn("Records screened to find every full-text inclusion | 1 (1 to 1) |", table)
