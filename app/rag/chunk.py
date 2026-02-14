from app.core.config import settings

def chunk_text(text: str) -> list[str]:
    text = (text or "").strip()
    if not text:
        return []

    size = settings.chunk_size
    overlap = settings.chunk_overlap

    if overlap >= size:
        overlap = size // 5

    chunks = []
    start = 0
    n = len(text)

    while start < n:
        end = min(n, start + size)
        chunks.append(text[start:end])
        if end == n:
            break
        start = end - overlap

    return chunks

