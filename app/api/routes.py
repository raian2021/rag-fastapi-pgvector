from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.security import require_api_key
from app.rag.ingest import ingest_plain_text
from app.rag.retrieve import retrieve
from app.rag.generate import generate_answer

router = APIRouter(prefix="/v1", tags=["rag"])

class IngestRequest(BaseModel):
    source: str
    text: str

class QueryRequest(BaseModel):
    question: str

@router.post("/ingest", dependencies=[Depends(require_api_key)])
def ingest(req: IngestRequest):
    return ingest_plain_text(req.source, req.text)

@router.post("/query", dependencies=[Depends(require_api_key)])
def query(req: QueryRequest):
    contexts = retrieve(req.question)
    gen = generate_answer(req.question, contexts)
    return {
        "answer": gen["answer"],
        "citations": gen["citations"],
        "retrieved": contexts,
    }

