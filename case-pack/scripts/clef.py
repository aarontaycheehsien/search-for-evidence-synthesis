"""Read CLEF TAR topic files and qrels.

Topic files have four sections: Topic, Title, Query and Pids. Qrels follow
the TREC format: topic, iteration, PMID, relevance.
"""

from pathlib import Path


def read_topic(path):
    """Return a dict with topic, title, query (list of lines) and pmids."""
    topic = {"topic": "", "title": "", "query": [], "pmids": []}
    section = None
    for raw in Path(path).read_text(encoding="utf-8", errors="replace").splitlines():
        line = raw.strip()
        if line.startswith("Topic:"):
            topic["topic"] = line[len("Topic:"):].strip()
            section = None
        elif line.startswith("Title:"):
            topic["title"] = line[len("Title:"):].strip()
            section = None
        elif line.startswith("Query:"):
            section = "query"
        elif line.startswith("Pids:"):
            section = "pmids"
        elif section == "query" and line:
            topic["query"].append(line)
        elif section == "pmids":
            topic["pmids"].extend(token for token in line.split() if token.isdigit())
    return topic


def read_qrels(path, topic=None):
    """Return {topic: {pmid: relevance}}, optionally for one topic only."""
    qrels = {}
    for line in Path(path).read_text(encoding="utf-8").splitlines():
        parts = line.split()
        if len(parts) < 4:
            continue
        topic_id, _, pmid, relevance = parts[:4]
        if topic and topic_id != topic:
            continue
        qrels.setdefault(topic_id, {})[pmid] = int(relevance)
    return qrels
