from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableSequence
from app.prompts.db_prompt import sql_prompt
from app.prompts.response_prompt import resp_prompt
from app.prompts.dberror_prompt import error_prompt
from app.config import settings
import os

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


llm = ChatOpenAI(model_name=settings.MODEL_ID, temperature=0.7)

#return_messages=True: Instead of returning the chat history as a plain string, 
#it returns a list of HumanMessage and AIMessage objects

#memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)

sql_chain = sql_prompt | llm
response_chain = resp_prompt | llm
dberror_chain = error_prompt | llm