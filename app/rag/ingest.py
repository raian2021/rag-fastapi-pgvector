from app.db.pgvector import insert_document, insert_chunk
from app.rag.chunk import chunk_text
from app.rag.embed import embed_texts

def ingest_plain_text(source: str, text: str) -> dict:
    doc_id = insert_document(source=source)
    chunks = chunk_text(text)

    if not chunks:
        return {"document_id": doc_id, "chunks_inserted": 0}

    embeddings = embed_texts(chunks)

    for i, (chunk, emb) in enumerate(zip(chunks, embeddings)):
        insert_chunk(
            document_id=doc_id,
            chunk_index=i,
            content=chunk,
            embedding=emb,
        )

    return {
        "document_id": doc_id,
        "chunks_inserted": len(chunks),
    }

