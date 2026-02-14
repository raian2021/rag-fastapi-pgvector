from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.core.config import settings
from app.db.pgvector import init_db
from app.api.routes import router

app = FastAPI(title=settings.app_name)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/", response_class=HTMLResponse)
def home():
    return f"""
    <html>
      <body style="font-family: Arial; max-width: 800px; margin: 40px auto;">
        <h1>{settings.app_name}</h1>
        <p>FastAPI + Postgres + pgvector RAG system.</p>
        <p>Docs: <a href="/docs">/docs</a></p>
      </body>
    </html>
    """

app.include_router(router)

