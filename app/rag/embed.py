from sentence_transformers import SentenceTransformer
from app.core.config import settings

_model = None


def get_embedder():
    global _model
    if _model is None:
        _model = SentenceTransformer(settings.embed_model)
    return _model


def _to_py_floats(vec) -> list[float]:
    """
    Ensure we return plain Python floats (not numpy float32/float64),
    which avoids pgvector casting/format edge cases.
    """
    # vec could be a numpy array; iterating yields numpy scalar types.
    return [float(x) for x in vec]


def embed_texts(texts: list[str]) -> list[list[float]]:
    model = get_embedder()
    vectors = model.encode(texts, normalize_embeddings=True)
    return [_to_py_floats(v) for v in vectors]


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]

