import json
import requests
from fastapi import HTTPException
from app.config import settings
from loguru import logger
from app.chains.llm_chain import sql_chain, dberror_chain
from app.crud.llm_response import sql_processor
from app.rag import search_vector
import logging
from typing import Dict, Any
from langchain_core.messages import AIMessage
from app.utils.response_perser import parse_ai_message
from app.crud.llm_response import sql_processor
from app.schemas.process_schema import LLMAction
from app.chains.llm_chain import response_chain
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from langchain_community.utilities import SQLDatabase
from app.virtual_file import run_chart_code


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_db_error(db: Session, query: str, schema: Dict[str, Any], parsed_response: Dict[str, Any], error: SQLAlchemyError) -> Dict[str, Any]:
    """Handle database errors by using dberror_chain to generate a user-friendly response.
    
    Args:
        query: The original user query
        schema: The vector search results
        parsed_response: The parsed response from the first LLM call
        error: The database error that occurred
    """
    try:
        error_message = str(error)
        logger.error(f"Database error occurred: {error_message}")

        logger.error(f"Processing the error")

        # Use dberror_chain to generate a helpful response with more context
        error_response = dberror_chain.invoke({
            "query": query,
            "schemas": schema,
            "response": parsed_response,
            "error": error
        })
        
        return parse_ai_message(error_response)
    except Exception as e:
        logger.error(f"Error in error handling: {str(e)}")
        return {
            "error": "I encountered an issue processing your request. Please try rephrasing your question.",
            "details": str(error)
        }

def vector_search(db: Session, query: str) -> Dict[str, Any]:
    try:
        logger.info(f"Processing vector search for query: {query}")
        # Get the search results
        #schema = search_vector(query)

        with open("db_schema.sql", "r") as file:
            schema_text = file.read()

        schema = schema_text

        print(schema)
        
        
        logger.info(f"Found {len(schema)} schema")

        logger.info("Sending schema to the llm as a sql_prompt")

        response = sql_chain.invoke({
            "schemas": schema,
            "question": query
        }) #, config={"configurable": {"session_id": "some-user-session-id"}})

        logger.info(f"LLM response: {response}")

        parsed_response = parse_ai_message(response)
        logger.info(f"parsed_response: {parsed_response}")

        llm_action = LLMAction(**parsed_response)

        if llm_action.action in ("question" or "logic"):
            return llm_action.dict()


        try:
            data = sql_processor(db, llm_action)
            logger.info(f"Data from database: {data}")

            second_response = response_chain.invoke({
                "question": query,
                "database_returned": data
            })

            final_response = parse_ai_message(second_response)
            logger.info(f"Final response: {final_response}")

            #llm_action_2 = LLMAction(**final_response)

            #if llm_action_2.action == "chart":
                #image_base64 = run_chart_code(llm_action.content)
                #return {
                    #"action": "chart",
                    #"image_base64": f"data:image/png;base64,{image_base64}"
                #}


            return final_response

        except SQLAlchemyError as db_error:
            return handle_db_error(db, query, schema, parsed_response, db_error)

    except Exception as e:
        logger.error(f"Error in vector_search: {e}")
        return {"success":False, "message": f"Something went wrong in vector search or chaining: {str(e)}"}


