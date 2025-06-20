from fastapi import APIRouter, HTTPException
from typing import Dict, Any
from app.schemas.chat_schema import AskRequest
from app.rag import embedding_model, insert_data, search_vector
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

router = APIRouter()

@router.post("/insert_vector", response_model=Dict[str, str], status_code=200)
def insert_db(request: AskRequest) -> Dict[str, str]:
    try:
        logger.info(f"Received insert request with query: {request.query}")
        prompt = request.query
        embeddings = embedding_model.get_embeddings([prompt])
        embedding_values = embeddings[0].values
        logger.info("Successfully generated embeddings")

        result = insert_data(prompt, embedding_values)
        logger.info("Successfully inserted data")
        return result
        
    except Exception as e:
        logger.error(f"Error in insert_vector: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Vector insertion failed: {str(e)}")

@router.post("/search_vector", response_model=Dict[str, Any], status_code=200)
def search_embeddings(request: AskRequest) -> Dict[str, Any]:
    try:
        logger.info(f"Received search request with query: {request.query}")
        results = search_vector(request.query)
        logger.info(f"Found {len(results)} results")
        return {"results": results}

    except Exception as e:
        logger.error(f"Error in search_vector: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Vector search failed: {str(e)}")