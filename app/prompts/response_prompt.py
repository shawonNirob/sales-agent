from langchain.prompts import PromptTemplate

resp_prompt = PromptTemplate( input_variable=["question", "database_returned"], template="""
    User Query:
    "{question}"

    Database returned:
    "{database_returned}"

    Do not ask too question to user. Provide your best response. and always try to provide the response in briefly.

    Respond ONLY in this JSON format:

    - if user asked for a graph or chart, genertae matplotlib code with the data and response like this:
    {{
        "action": "chart",
        "content": "a runable python code with matplotlib, numpy, pandas library"
    }}

    - response to the user like this:
    {{
        "action": "response",
        "content": "<a clear natural language response to the user>"
    }}

    """
)