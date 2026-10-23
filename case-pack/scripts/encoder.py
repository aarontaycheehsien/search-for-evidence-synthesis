"""A small sentence encoder for the case pack: all-MiniLM-L6-v2 in ONNX form.

The model is the sentence-transformers all-MiniLM-L6-v2 encoder, as exported
to ONNX and distributed by Chroma. It is downloaded once into
case-pack/cache/models/ (which Git ignores) and checked against the
SHA-256 recorded below, so every rebuild uses the same weights.

Embeddings follow the model's documented recipe: tokenise, truncate to 256
word pieces, run the encoder, average the token vectors over the attention
mask, and normalise to unit length, so a dot product is a cosine similarity.

Requires: onnxruntime, tokenizers, numpy.
"""

import hashlib
import sys
import tarfile
import urllib.request
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))

from common import CACHE  # noqa: E402

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_URL = "https://chroma-onnx-models.s3.amazonaws.com/all-MiniLM-L6-v2/onnx.tar.gz"
MODEL_SHA256 = "913d7300ceae3b2dbc2c50d1de4baacab4be7b9380491c27fab7418616a16ec3"
MAX_TOKENS = 256
BATCH = 64


def model_dir():
    """Download and unpack the model if needed; return the folder holding model.onnx."""
    root = CACHE / "models" / "all-MiniLM-L6-v2"
    folder = root / "onnx"
    if (folder / "model.onnx").exists():
        return folder
    root.mkdir(parents=True, exist_ok=True)
    archive = root / "onnx.tar.gz"
    if not archive.exists():
        urllib.request.urlretrieve(MODEL_URL, archive)
    digest = hashlib.sha256(archive.read_bytes()).hexdigest()
    if digest != MODEL_SHA256:
        raise RuntimeError(f"Unexpected checksum for {archive}: {digest}")
    with tarfile.open(archive) as tar:
        tar.extractall(root, filter="data")
    return folder


class Encoder:
    def __init__(self, folder=None):
        import onnxruntime
        from tokenizers import Tokenizer

        folder = Path(folder) if folder else model_dir()
        self.tokenizer = Tokenizer.from_file(str(folder / "tokenizer.json"))
        self.counter = Tokenizer.from_file(str(folder / "tokenizer.json"))
        self.counter.no_truncation()
        self.counter.no_padding()
        self.tokenizer.enable_truncation(max_length=MAX_TOKENS)
        self.tokenizer.enable_padding(pad_id=0, pad_token="[PAD]")
        self.session = onnxruntime.InferenceSession(
            str(folder / "model.onnx"), providers=["CPUExecutionProvider"])

    def token_count(self, text):
        """Word pieces in the text, including the two special tokens, before truncation."""
        return len(self.counter.encode(text).ids)

    def embed(self, texts):
        vectors = []
        for start in range(0, len(texts), BATCH):
            batch = self.tokenizer.encode_batch(texts[start:start + BATCH])
            ids = np.array([e.ids for e in batch], dtype=np.int64)
            mask = np.array([e.attention_mask for e in batch], dtype=np.int64)
            hidden = self.session.run(None, {
                "input_ids": ids, "attention_mask": mask, "token_type_ids": np.zeros_like(ids),
            })[0]
            weights = mask[..., None]
            pooled = (hidden * weights).sum(axis=1) / weights.sum(axis=1)
            vectors.append(pooled / np.linalg.norm(pooled, axis=1, keepdims=True))
        return np.vstack(vectors)
