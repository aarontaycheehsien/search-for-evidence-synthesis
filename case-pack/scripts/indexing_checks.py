"""Emulate the running cases' MEDLINE strategy lines on included records.

For each included record of CD010558 and CD011787 that has a PubMed
record, this script asks which lines of the review's Ovid MEDLINE strategy
admit it: subject headings, publication types, text words or search
filters. It reads PubMed records cached by a separate fetch (titles,
abstracts, MeSH headings, publication types and language) and writes one
row of true/false values per record. No title or abstract text is written.

The emulation approximates Ovid MEDLINE; it is not Ovid:

- Text is lower-cased and split into words at every character that is not
  a letter or digit, so "double-blind" and "re-uptake" become two words.
- In search terms, * and : truncate without limit, # stands for exactly one
  character and ? for zero or one character.
- "adjN" is treated as: within N words of each other, in either order, in
  the same field.
- ti is the title, ab the abstract and hw the words of the MeSH headings.
  mp is treated as title, abstract and heading words. Author keywords (kf)
  and other Ovid fields are not available and are treated as empty.
- "Heading/" matches a MeSH heading exactly; "exp Heading/" is treated the
  same way, so narrower headings are not included. Publication types are
  matched against PubMed's list for the record.
- MeSH headings and publication types are as PubMed holds them on the
  fetch date, which may differ from when the strategy was run.
- Entry-date (ed) limits are not emulated; see the reference-set README.

Usage:
  python case-pack/scripts/indexing_checks.py
    (reads case-pack/cache/pubmed/records.json; writes
    case-pack/data/indexing/CD010558-lines.csv and CD011787-lines.csv)
"""

import csv
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CACHE, CASE_PACK, DATA  # noqa: E402

WORD = re.compile(r"[a-z0-9]+")


def words(text):
    return WORD.findall((text or "").lower())


def _token_pattern(token):
    out = ""
    for ch in token.lower():
        if ch in "*:":
            out += "[a-z0-9]*"
        elif ch == "#":
            out += "[a-z0-9]"
        elif ch == "?":
            out += "[a-z0-9]?"
        else:
            out += re.escape(ch)
    return re.compile(out + r"\Z")


class Terms:
    """Any of several terms; a term with spaces or hyphens is a phrase."""

    def __init__(self, *terms):
        self.phrases = [[_token_pattern(t) for t in re.split(r"[\s-]+", term) if t] for term in terms]

    def spans(self, tokens):
        found = []
        for phrase in self.phrases:
            n = len(phrase)
            for i in range(len(tokens) - n + 1):
                if all(p.match(tokens[i + k]) for k, p in enumerate(phrase)):
                    found.append((i, i + n - 1))
        return found


class Adj:
    """Two expressions within n words of each other, in either order."""

    def __init__(self, left, right, n):
        self.left, self.right, self.n = left, right, n

    def spans(self, tokens):
        found = []
        for a in self.left.spans(tokens):
            for b in self.right.spans(tokens):
                if b[0] > a[1]:
                    gap = b[0] - a[1]
                elif a[0] > b[1]:
                    gap = a[0] - b[1]
                else:
                    continue
                if gap <= self.n:
                    found.append((min(a[0], b[0]), max(a[1], b[1])))
        return found


class Any:
    def __init__(self, *exprs):
        self.exprs = exprs

    def spans(self, tokens):
        return [s for e in self.exprs for s in e.spans(tokens)]


class Record:
    def __init__(self, data):
        self.pmid = data["pmid"]
        self.headings = {h.lower() for h in data.get("mesh_terms") or []}
        self.types = {t.lower() for t in data.get("article_types") or []}
        self.language = (data.get("language") or "").lower()
        self.journal = (data.get("journal") or "").lower()
        self.fields = {
            "ti": [words(data.get("title"))],
            "ab": [words(data.get("abstract"))],
            "hw": [words(h) for h in data.get("mesh_terms") or []],
            "kf": [],
        }
        self.fields["mp"] = self.fields["ti"] + self.fields["ab"] + self.fields["hw"]

    def has(self, expr, fields):
        return any(expr.spans(tokens) for f in fields.split(",") for tokens in self.fields[f])

    def all_of(self, exprs, fields):
        """Ovid's AND within one line: each part may match in any listed field."""
        return all(self.has(e, fields) for e in exprs)

    def heading(self, *names):
        return any(n.lower() in self.headings for n in names)

    def pub_type(self, *names):
        return any(n.lower() in self.types for n in names)


# CD010558: Psychological therapies for treatment-resistant depression.

DEPRESS = Terms("depress*")
SEROTONIN = Adj(Terms("serotonin"), Terms("uptake", "reuptake", "re-uptake"), 3)


def cd010558_lines(r):
    line = {}
    line[1] = r.heading("Depressive Disorder, Treatment-Resistant")
    failing = Any(Terms("antidepress*", "SSRI*", "SNRI*", "medication*", "psychotropic", "treatment*", "respon*"), SEROTONIN)
    line[2] = r.all_of([DEPRESS, Adj(failing, Terms("fail*"), 2)], "ti,ab,kf")
    nonresponse = Any(Terms("antidepress*", "SSRI*", "SNRI*", "psychotropic medication*", "treatment*"), SEROTONIN)
    line[3] = r.all_of(
        [DEPRESS, Adj(nonresponse, Terms("no respon*", "not respon*", "nonrespon*", "non-respon*", "unrespon*"), 2)], "ti,ab,kf"
    )
    line[4] = r.has(Adj(DEPRESS, Terms("refractor*", "resistan*", "chronic*", "persist*"), 3), "ti,ab,kf")
    line[5] = r.has(Adj(DEPRESS, Terms("relaps*", "recurr*"), 3), "ti,kf")
    line[6] = r.all_of([DEPRESS, Terms("augment*", "potentiat*")], "mp")
    line[7] = any(line[i] for i in range(1, 7))

    line[8] = r.pub_type("Randomized Controlled Trial") or r.heading("Randomized Controlled Trials as Topic")
    line[9] = r.pub_type("Controlled Clinical Trial")
    line[10] = r.has(
        Any(
            Terms("RCT", "randomi#ed", "at random"),
            Adj(Terms("random*"), Terms("assign*", "allocat*", "divide*", "division", "number*"), 3),
        ),
        "ti,ab,kf",
    )
    line[11] = r.all_of([Terms("placebo", "sham", "mock", "fake", "dummy"), Terms("control*", "group?")], "ti,ab,kf")
    line[12] = r.has(Terms("double-blind*"), "ti,ab,kf,hw")
    line[13] = r.has(Terms("trial"), "ti")
    line[14] = r.has(
        Adj(Terms("cluster", "crossover*", "cross-over*"), Terms("random*", "trial", "study", "control*", "group?"), 3), "ti,ab,kf"
    )
    line[15] = any(line[i] for i in range(8, 15))
    line[16] = line[7] and line[15]

    line[17] = r.pub_type("Letter")
    line[18] = r.pub_type("Editorial")
    line[19] = r.pub_type("News")
    line[20] = r.pub_type("Historical Article")
    line[21] = r.heading("Anecdotes as Topic")
    line[22] = r.pub_type("Comment")
    line[23] = r.pub_type("Case Reports")
    line[24] = r.has(Terms("letter", "comment*"), "ti")
    line[25] = r.heading("Animals") and not r.heading("Humans")
    line[26] = r.heading("Animals, Laboratory")
    line[27] = r.heading("Animal Experimentation") and not (r.heading("Human Experimentation") or r.heading("Humans"))
    line[28] = r.heading("Models, Animal")
    line[29] = r.heading("Rodentia")
    line[30] = r.has(Terms("rat", "rats", "mouse", "mice", "rodent*"), "ti")
    line[31] = any(line[i] for i in range(17, 31))
    line[32] = line[16] and not line[31]
    return line


def cd010558_row(r):
    line = cd010558_lines(r)
    return {
        "condition_heading": line[1],
        "condition_text": any(line[i] for i in range(2, 7)),
        "condition_block": line[7],
        "design_publication_type": line[8] or line[9],
        "design_text": any(line[i] for i in range(10, 15)),
        "design_block": line[15],
        "removed_by_not_block": line[16] and line[31],
        "admitted_before_date_limit": line[32],
    }


# CD011787: communication about childhood vaccination (qualitative).

VACCINE = Terms("vaccin*", "revaccinat*", "immuniz*", "immunis*")
VACCINATE = Terms("vaccinat*", "revaccinat*", "immuniz*", "immunis*")
COMMUNICATION = Terms("communicat*", "inform*", "rumor*", "promot*", "discuss*", "persua*", "motivat*", "empower*", "counsel*", "educat*")
MEDIA = Terms(
    "mass media", "media campaign*", "social media?", "network*", "net work*", "telephon*", "phone*", "hotline*", "hot line*",
    "answering service*", "reminder?", "radio", "television", "online", "on line web", "internet", "e mail*", "sms",
    "text message*", "messaging", "blog?", "blogging", "face book", "facebook", "twitter", "e health", "m health",
    "pamphlet?", "brochure?", "booklet?",
)
DECISION = Terms("decide", "deciding", "decision*", "consent*")
UNDERSTANDING = Terms("understand*", "comprehen*", "knowledge", "skill", "skills", "literacy")
ATTITUDE = Terms("attitud*", "perception*", "perceiv*", "aware*", "uncertain*", "hesitan*")
ACCEPTANCE = Terms(
    "accept*", "willing*", "concern", "concerns", "concerned", "objection?", "against", "reject", "refus*", "resist*",
    "anxiety", "anxious", "feeling?", "emotion*",
)

VACCINATION_HEADINGS = ["Immunization", "Immunization Programs", "Immunization, Schedule", "Vaccination", "Mass Vaccination", "Vaccines"]
POPULATION_HEADINGS = [
    "Child", "Child, Preschool", "Infant", "Infant, Newborn", "Child Care", "Infant Care", "Child Welfare", "Mothers",
    "Pregnant Women", "Fathers", "Parents", "Parenting", "Maternal Behavior", "Paternal Behavior",
]
COMMUNICATION_HEADINGS = [
    "Correspondence as Topic", "Communication", "Communication Barriers", "Health Communication", "Persuasive Communication",
    "Propaganda", "Communications Media", "Mass Media", "Internet", "Blogging", "Social Media", "Social Networking", "Radio",
    "Television", "Telephone", "Cellular Phone", "Text Messaging", "Electronic Mail", "Answering Services", "Reminder Systems",
    "Hotlines", "Health Promotion", "Social Marketing", "Marketing of Health Services", "Health Education", "Counseling",
    "Motivation", "Information Dissemination", "Consumer Health Information", "Patient Education as Topic", "Pamphlets",
    "Information Literacy", "Health Literacy", "Information Seeking Behavior", "Knowledge", "Comprehension",
    "Health Knowledge, Attitudes, Practice", "Attitude to Health", "Patient Acceptance of Health Care", "Power (Psychology)",
    "Decision Making", "Decision Support Techniques", "Uncertainty", "Perception",
]
LANGUAGES = {"dan", "eng", "fre", "nor", "swe"}


def ovid_qualitative_sensitive(r):
    """Ovid's "qualitative (maximizes sensitivity)" limit; see QUALITATIVE_FILTER_SOURCE."""
    return r.has(Terms("interview:", "experience:"), "mp") or r.has(Terms("qualitative"), "ti,ab")


QUALITATIVE_FILTER_SOURCE = "set after checking the Ovid and HIRU documentation"


def cd011787_lines(r):
    line = {}
    line[7] = r.heading(*VACCINATION_HEADINGS)
    population_text = r.has(Terms("child*", "infant*", "newborn*", "new born*", "neonat*", "baby", "babies", "toddler*"), "ti,ab") or r.has(
        Terms("mother*", "pregnant women", "father*", "parent*"), "ti,ab"
    )
    line["24_headings"] = r.heading(*POPULATION_HEADINGS)
    line[24] = line["24_headings"] or population_text
    line[69] = r.heading(*COMMUNICATION_HEADINGS)
    line[70] = line[7] and line[24] and line[69]
    pairs = [
        (COMMUNICATION, VACCINE, VACCINATE),
        (MEDIA, VACCINE, VACCINE),
        (DECISION, VACCINE, VACCINATE),
        (UNDERSTANDING, VACCINE, VACCINATE),
        (ATTITUDE, VACCINE, VACCINE),
        (ACCEPTANCE, VACCINE, VACCINE),
    ]
    line[83] = any(r.all_of([group, vti], "ti") or r.has(Adj(group, vab, 6), "ab") for group, vti, vab in pairs)
    line[84] = line[83] and line[24]
    line[85] = line[70] or line[84]
    line[86] = line[85] and ovid_qualitative_sensitive(r)
    line[87] = r.heading("Qualitative Research", "Interviews as Topic") or r.has(
        Terms("qualitative", "group discussion?", "focus group?", "themes"), "ti,ab"
    )
    line[88] = line[85] and line[87]
    line[89] = line[86] or line[88]
    animals_only = r.heading("Animals") and not r.heading("Humans")
    excluded_types = r.pub_type("Review", "Meta-Analysis", "News", "Comment", "Editorial")
    line[101] = (
        animals_only
        or excluded_types
        or r.journal == "the cochrane database of systematic reviews"
        or r.has(Terms("systematic review", "literature review"), "ti")
    )
    line[102] = line[89] and not line[101]
    line[103] = line[102] and r.language in LANGUAGES
    return line


def cd011787_row(r):
    line = cd011787_lines(r)
    return {
        "subject_route_headings": line[70],
        "subject_route_text": line[84],
        "subject_block": line[85],
        "ovid_qualitative_filter": ovid_qualitative_sensitive(r),
        "custom_qualitative_block": line[87],
        "qualitative_requirement_met": line[89],
        "removed_by_not_block": line[89] and line[101],
        "language_limit_met": r.language in LANGUAGES,
        "admitted_before_date_limit": line[103],
    }


def load_records(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    return {str(r["pmid"]): r for r in data["records"]}


def reference_rows(review):
    path = CASE_PACK / "reference-sets" / f"{review}.csv"
    seen, rows = set(), []
    for row in csv.DictReader(path.open(encoding="utf-8")):
        if row["pmid"] and row["pmid"] not in seen:
            seen.add(row["pmid"])
            rows.append(row)
    return rows


def write(review, row_function, records, out_dir):
    rows = []
    for ref in reference_rows(review):
        record = records.get(ref["pmid"])
        if record is None:
            raise SystemExit(f"{ref['pmid']} is not in the cached records")
        flags = row_function(Record(record))
        rows.append({
            "pmid": ref["pmid"],
            "study_id": ref["study_id"],
            "year": record.get("year") or "",
            "in_clef_pool": ref["in_clef_pool"],
            **{k: int(v) for k, v in flags.items()},
        })
    out = out_dir / f"{review}-lines.csv"
    with out.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows


def main():
    records = load_records(CACHE / "pubmed" / "records.json")
    out_dir = DATA / "indexing"
    out_dir.mkdir(parents=True, exist_ok=True)
    for review, function in (("CD010558", cd010558_row), ("CD011787", cd011787_row)):
        rows = write(review, function, records, out_dir)
        print(review, len(rows), "records")
        for key in rows[0]:
            if key in ("pmid", "study_id", "year", "in_clef_pool"):
                continue
            in_pool = sum(r[key] for r in rows if r["in_clef_pool"] == "1")
            print(f"  {key}: {sum(r[key] for r in rows)} of {len(rows)} ({in_pool} of {sum(r['in_clef_pool'] == '1' for r in rows)} in pool)")


if __name__ == "__main__":
    main()
