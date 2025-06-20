from fastapi import APIRouter, HTTPException, Depends
from app.schemas.chat_schema import AskRequest
from app.chains.agent_chain import vector_search
import logging
from typing import Dict, Any
from app.db import get_db

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

QUERY_CHAR_LIMIT = 500

@router.post("/ask", response_model=Dict[str, Any], status_code=200)
def ask(request: AskRequest, db=Depends(get_db)) -> Dict[str, Any]:
    if len(request.query) > QUERY_CHAR_LIMIT:
        return {"error": "Query size exceeded", "allowed_limit": QUERY_CHAR_LIMIT}

    try:
        logger.info(f"Received ask request with query: {request.query}")
        return vector_search(db, request.query)
    except Exception as e:
        logger.error(f"Error in ask endpoint: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/reset")
def reset_memory():
    return{"development is not finish yet"}
