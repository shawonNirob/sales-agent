from langchain_community.utilities import SQLDatabase

db = SQLDatabase.from_uri("mysql+pymysql://root:Admin123!@localhost:3306/org_flow")

print("Here is the schema:")
print(db.get_table_info())


