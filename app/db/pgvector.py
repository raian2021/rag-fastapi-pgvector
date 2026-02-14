from psycopg import connect
from psycopg.rows import dict_row

from app.core.config import settings

EMBED_DIM = 384  # all-MiniLM-L6-v2


def to_vec_str(v: list[float]) -> str:
    """
    Canonical pgvector text format (fixed decimals; no scientific notation).
    Example: [0.12345678,-0.00001234,...]
    """
    return "[" + ",".join(f"{float(x):.8f}" for x in v) + "]"


import psycopg

def get_conn():
    conn = psycopg.connect(
        host=settings.db_host,
        dbname=settings.db_name,
        user=settings.db_user,
        password=settings.db_password,
        row_factory=psycopg.rows.dict_row,
    )
    conn.autocommit = True
    return conn


def init_db():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS documents (
                    id BIGSERIAL PRIMARY KEY,
                    source TEXT NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                f"""
                CREATE TABLE IF NOT EXISTS chunks (
                    id BIGSERIAL PRIMARY KEY,
                    document_id BIGINT NOT NULL REFERENCES documents(id) ON DELETE CASCADE,
                    chunk_index INT NOT NULL,
                    content TEXT NOT NULL,
                    embedding vector({EMBED_DIM}) NOT NULL,
                    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
                );
                """
            )

            cur.execute(
                """
                CREATE INDEX IF NOT EXISTS idx_chunks_document_id
                ON chunks(document_id);
                """
            )

            conn.commit()


def insert_document(source: str) -> int:
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute("INSERT INTO documents (source) VALUES (%s) RETURNING id;", (source,))
            doc_id = cur.fetchone()["id"]
            conn.commit()
            return int(doc_id)


def insert_chunk(document_id: int, chunk_index: int, content: str, embedding: list[float]) -> int:
    vec = to_vec_str(embedding)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                f"""
                INSERT INTO chunks (document_id, chunk_index, content, embedding)
                VALUES (%s, %s, %s, (%s)::vector({EMBED_DIM}))
                RETURNING id;
                """,
                (document_id, chunk_index, content, vec),
            )
            chunk_id = cur.fetchone()["id"]
            conn.commit()
            return int(chunk_id)


def search_chunks(query_embedding: list[float], top_k: int):
    vec = to_vec_str(query_embedding)

    sql = f"""
    SELECT
        c.id,
        c.document_id,
        c.chunk_index,
        c.content,
        (c.embedding <#> (%s)::vector({EMBED_DIM})) AS distance,
        d.source
    FROM chunks c
    JOIN documents d ON d.id = c.document_id
    ORDER BY distance
    LIMIT %s;
    """

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(sql, (vec, int(top_k)))
            return list(cur.fetchall())

