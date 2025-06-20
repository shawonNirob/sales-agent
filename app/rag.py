import os
import json 
import vertexai
from vertexai.language_models import TextEmbeddingModel
import singlestoredb as s2 
from app.config import settings
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from typing import Dict, List, Any
import logging
from app.schemas.chat_schema import AskRequest

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/shawon/builder/chain-llm/erp-ai-agent-backup/db-chatbot-ai/vertexai_service_key.json"

PROJECT_ID = "innate-node-453604-g7"
vertexai.init(project=PROJECT_ID, location="us-central1")

embedding_model = TextEmbeddingModel.from_pretrained("text-multilingual-embedding-002")

S2_CON_STRING = settings.S2_STRING

def insert_data(prompt: str, embedding_values: List[float]) -> Dict[str, str]:
    try:
        logger.info(f"Attempting to connect to SingleStore with connection string: {S2_CON_STRING[:10]}...")
        with s2.connect(S2_CON_STRING) as conn:
            embedding_json = json.dumps(embedding_values)
            logger.info("Successfully converted embeddings to JSON")

            #tuple to match the placeholders in the SQL statement (%s).
            data = (prompt, embedding_json)
            stmt = 'insert into textVector(text, vector) values (%s, JSON_ARRAY_PACK(%s))'
            logger.info("Executing insert statement")
            with conn.cursor() as cur:
                cur.execute(stmt, data)
                logger.info("Successfully executed insert statement")
                return {"message": "Data inserted successfully"}

    except IntegrityError as e:
        logger.error(f"Integrity error during insertion: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Vector insertion failed due to integrity error."
        )
    except Exception as e:
        logger.error(f"Error during insertion: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector insertion failed: {str(e)}"
        )

def search_vector(query: str) -> Dict[str, Any]:
    try:
        logger.info("Generating embeddings for search query")
        query_embedding = embedding_model.get_embeddings([query])[0].values
        query_vector = json.dumps(query_embedding)
        logger.info("Successfully generated embeddings for search")

        stmt = '''
        select text, dot_product(vector, JSON_ARRAY_PACK(%s)) as score
        from textVector
        order by score desc
        limit 4;
        '''

        logger.info("Attempting to connect to SingleStore for search")
        with s2.connect(S2_CON_STRING) as conn:
            with conn.cursor() as cur:
                logger.info("Executing search query")
                cur.execute(stmt, (query_vector,))
                results = cur.fetchall()
                logger.info(f"Found {len(results)} results")
                return [{"text": row[0], "score": float(row[1])} for row in results]

    except Exception as e:
        logger.error(f"Error during search: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Vector search failed: {str(e)}"
        )


#prompt = "Hello Bot"

#embeddings = embedding_model.get_embeddings([prompt])
#embedding_values = embeddings[0].values

#insert_data(prompt, embedding_values)
#search_embeddings("Hello")

