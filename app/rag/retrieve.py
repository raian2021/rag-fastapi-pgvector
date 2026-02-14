from app.core.config import settings
from app.db.pgvector import search_chunks
from app.rag.embed import embed_query


def retrieve(query: str) -> list[dict]:
    q_emb = embed_query(query)
    rows = search_chunks(q_emb, settings.top_k)

    # ✅ Deduplicate by content (keeps best-ranked first)
    seen = set()
    deduped = []
    for r in rows:
        content = (r.get("content") or "").strip()
        if not content:
            continue
        if content in seen:
            continue
        seen.add(content)
        deduped.append(r)

    results = []
    for r in deduped:
        score = 1.0 - float(r["distance"])
        results.append({
            "chunk_id": r["id"],
            "document_id": r["document_id"],
            "chunk_index": r["chunk_index"],
            "source": r["source"],
            "content": r["content"],
            "score": score,
        })

    return results

