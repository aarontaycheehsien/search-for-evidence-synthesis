"""Offline tests for the case-pack scripts.

Run from the repository root:
  python -m unittest discover -s case-pack/tests
"""

import math
import sys
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent / "scripts"))

from analyser_checks import hyphen_kept, min_gap  # noqa: E402
from build_moran_pool import build  # noqa: E402
from capture_recapture import estimate  # noqa: E402
from clef import read_qrels, read_topic  # noqa: E402
from clef_label_scope import scope  # noqa: E402
from common import normalise_doi  # noqa: E402
from field_checks import check as moran_check  # noqa: E402
from fetch_pubmed import parse_efetch, reference_set_pmids  # noqa: E402
from indexing_checks import Adj, Record, Terms, cd010558_row, words  # noqa: E402
from ranking_measures import measures as ranking_measures  # noqa: E402
from pipeline_checks import rerank, rrf, union_top  # noqa: E402
from representation_checks import neighbour_labels  # noqa: E402
from ranking_checks import bm25_scores, expand, expected_last_rank, ranks, recall_at  # noqa: E402
from stopping_checks import first_stop, read_log  # noqa: E402
from term_mining import mine, split  # noqa: E402

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

    def test_expected_last_rank_in_random_order(self):
        # One eligible record among n sits, on average, in the middle.
        self.assertEqual(expected_last_rank(9, 1), 5)
        # Brute force over every placement of two eligible records among four.
        from itertools import combinations
        places = list(combinations(range(1, 5), 2))
        self.assertAlmostEqual(expected_last_rank(4, 2), sum(max(p) for p in places) / len(places))


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
        self.assertIn("Randomized Controlled Trial", first["article_types"])
        self.assertEqual(first["mesh_terms"], ["Depressive Disorder, Treatment-Resistant"])
        self.assertEqual(first["doi"], "10.9999/synthetic.0001")
        self.assertEqual(first["year"], "2016")
        self.assertEqual(first["journal"], "Synthetic journal of trials")
        self.assertEqual(first["journal_abbreviation"], "Synth J")
        self.assertEqual(first["language"], "eng")

    def test_output_feeds_the_indexing_scripts(self):
        record = Record(self.records[0])
        self.assertEqual(record.headings, {"depressive disorder, treatment-resistant"})
        self.assertIn("randomized controlled trial", record.types)
        self.assertEqual(record.language, "eng")
        self.assertTrue(record.has(Terms("synthetic"), "ti"))

    def test_reference_set_pmids(self):
        pmids = reference_set_pmids([HERE.parent / "reference-sets" / "CD010558.csv"])
        self.assertTrue(pmids)
        self.assertTrue(all(p.isdigit() for p in pmids))
        self.assertEqual(len(pmids), len(set(pmids)))

    def test_missing_parts(self):
        second = self.records[1]
        self.assertEqual(second["abstract"], "")
        self.assertEqual(second["date_completed"], "")
        self.assertEqual(second["status"], "In-Process")
        self.assertEqual(second["doi"], "")
        self.assertEqual(second["year"], "")
        self.assertEqual(second["journal"], "Synth J")
        self.assertEqual(second["language"], "")


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


class TermMiningTest(unittest.TestCase):
    def test_split_is_fixed_and_complete(self):
        ids = [str(i) for i in range(137)]
        dev, val = split(ids)
        self.assertEqual((len(dev), len(val)), (69, 68))
        self.assertEqual(dev | val, set(ids))
        self.assertEqual(split(ids), (dev, val))

    def test_mine_keeps_common_failure_words_rare_in_pool(self):
        tokens = {
            "a": ["conspecific", "foraging", "|"],
            "b": ["conspecific", "|", "common"],
            **{f"p{i}": ["common", "|"] for i in range(40)},
        }
        pool_df = {}
        for t in tokens.values():
            for w in set(t):
                pool_df[w] = pool_df.get(w, 0) + 1
        words_found = [w for _, w, _, _ in mine(["a", "b"], tokens, pool_df, len(tokens))]
        self.assertEqual(set(words_found), {"conspecific", "foraging"})


class RankingMeasuresTest(unittest.TestCase):
    def test_measures_on_a_small_ranking(self):
        m = ranking_measures([3, 1], 10)
        self.assertAlmostEqual(m["ap"], (1 + 2 / 3) / 2)
        self.assertAlmostEqual(m["ndcg"], 1.5 / (1 + 1 / math.log2(3)))
        self.assertEqual((m["first"], m["at95"], m["last"]), (1, 3, 3))
        self.assertAlmostEqual(m["wss95"], 0.65)
        self.assertEqual(m["recall_10pct"], 0.5)


class PipelineChecksTest(unittest.TestCase):
    def test_rerank_reorders_only_the_candidates(self):
        first = [1, 2, 3, 4, 5]
        second = [5, 4, 3, 2, 1]
        self.assertEqual(rerank(first, second, 3), [3, 2, 1, 4, 5])

    def test_rrf_prefers_records_both_rankings_like(self):
        self.assertEqual(rrf([1, 2, 3], [3, 1, 2], k=60), [2, 1, 3])

    def test_union_of_top_candidates(self):
        self.assertEqual(union_top([1, 2, 3, 4], [4, 3, 2, 1], 2), {0, 1, 2, 3})
        self.assertEqual(union_top([1, 2, 3, 4], [2, 1, 3, 4], 2), {0, 1})


class RepresentationChecksTest(unittest.TestCase):
    def test_neighbour_labels_counts_nearest_records(self):
        import numpy as np
        vectors = np.array([[1.0, 0.0], [0.9, 0.1], [0.0, 1.0], [0.1, 0.9]])
        vectors = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        ta = np.array([1, 1, 1, 0])
        ft = np.array([1, 0, 1, 0])
        first, counts = neighbour_labels(vectors, ta, ft, 1)
        self.assertEqual(first, {"included": 0, "title and abstract only": 1, "excluded": 1})
        self.assertEqual(counts, first)


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


class StoppingChecksTest(unittest.TestCase):
    def test_read_log_pads_missing_ranks(self):
        path = FIXTURES / "stopping_log_synthetic.csv"
        path.write_text("rank,id,label_title_abstract,label_full_text\n1,a,1,1\n3,c,1,\n")
        try:
            ta, ft = read_log(path, 5)
        finally:
            path.unlink()
        self.assertEqual(ta, [1, 0, 1, 0, 0])
        self.assertEqual(ft, [1, 0, 0, 0, 0])

    def test_first_stop_checks_every_five_once_something_is_relevant(self):
        calls = []

        def fake_h0(labels, n_total, recall_target):
            calls.append(len(labels))
            return 0.01 if len(labels) >= 12 else 0.5

        self.assertEqual(first_stop([0] * 6 + [1] + [0] * 13, 20, fake_h0), 15)
        self.assertEqual(calls, [10, 15])

    def test_first_stop_never(self):
        self.assertIsNone(first_stop([1] * 10, 10, lambda *args, **kwargs: 0.5))


class CaptureRecaptureTest(unittest.TestCase):
    def test_reproduces_spoor_1996(self):
        # Spoor et al. (1996): 115 found by both, 35 by hand search only,
        # 8 by Medline only; reported total 160 (95% CI 158 to 164).
        result = estimate(115, 35, 8)
        self.assertEqual(result["found"], 158)
        self.assertEqual(round(result["chapman"]), 160)
        self.assertEqual(result["chapman_low"], 158)
        self.assertEqual(round(result["chapman_high"]), 164)


class FieldChecksTest(unittest.TestCase):
    def test_moran_blocks_on_title_and_abstract(self):
        hit = moran_check("Hunger increases boldness",
                          "Starved fish showed bolder behaviour in response to a novel object.")
        self.assertEqual(hit, {"condition": True, "risk": True, "behaviour": True})

    def test_proximity_window_for_food_terms(self):
        near = moran_check("Food availability and boldness", "Personality was measured.")
        far = moran_check("Food was given once a day in the laboratory with no change in "
                          "availability", "Boldness and personality were measured.")
        self.assertTrue(near["condition"])
        self.assertFalse(far["condition"])
