from fastapi import HTTPException
from loguru import logger
from app.schemas.process_schema import LLMAction
from app.crud.db_crud import crud_operation
from typing import Dict, Any
import logging
from sqlalchemy.orm import Session

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def sql_processor(db: Session, data: LLMAction) -> Dict[str, Any]:
    try:
        logger.info(f"Received LLMAction: {data}")
        action = data.action
        content = data.content

        logger.info(f"Action: {action}")
        logger.info(f"Content: {content}")

        if action == "singleSQL":
            logger.info("Processing singleSQL action")
            result = crud_operation(db, content)
            logger.info(f"Result from singleSQL: {result}")
            return result

        elif action == "multipleSQL":
            logger.info("Processing multipleSQL action")
            if isinstance(content, list):
                results = []
                for sql in content:
                    logger.info(f"Executing SQL: {sql}")
                    result = crud_operation(db, sql)
                    logger.info(f"Result for SQL: {result}")
                    results.append(result)
                logger.info(f"All results from multipleSQL: {results}")
                return results

            elif isinstance(content, str):
                logger.info(f"Content is string, executing single SQL from multipleSQL action: {content}")
                result = crud_operation(db, content)
                logger.info(f"Result: {result}")
                return result

        elif action == "question":
            logger.info("Processing question action")
            return {"action": "question", "content": content}

        elif action == "logic":
            logger.info("Processing logic action")
            return {"action": "logic", "content": content}

        else:
            logger.warning(f"Unknown action received: {action}")
            return {"error": "Unknown action in LLM response"}

    except Exception as e:
        logger.error(f"LLM processing failed: {str(e)}")
        return {"success": False, "message": f"LLM response is not sructured for proceess: {str(e)}"}
