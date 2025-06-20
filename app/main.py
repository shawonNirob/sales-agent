from fastapi import FastAPI, Depends
from sqlalchemy import text
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_db
from app.api.routes.chat import router as chat_router
from app.api.routes.vector_embeddings import router as vector_router

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(chat_router, prefix="/agent", tags=["chat"])
app.include_router(vector_router, prefix="/vector", tags=["vector"])

@app.get("/")
def read_root():
    return {"message": "Welcome to Database AI Agent"}

@app.get("/_status")
def read_status():
    return {"status": "ok"}

@app.get("/_db_status")
def db_status(db = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"status": "ok"}
    except Exception as e:
        return {"status": "error", "message": str(e)}




