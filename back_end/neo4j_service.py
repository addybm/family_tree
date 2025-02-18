from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import bcrypt

# # Load environment variables
# load_dotenv()

# # Neo4j Connection
# driver = GraphDatabase.driver(
#     os.getenv("NEO4J_URI"), 
#     auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
# )

# def get_people():
#     with driver.session() as session:
#         result = session.run("MATCH (p:Person) RETURN p.name AS name")
#         return [record["name"] for record in result]


class Neo4jService:
    def __init__(self):
        self.driver = GraphDatabase.driver(
            os.getenv("NEO4J_URI"), 
            auth=(os.getenv("NEO4J_USERNAME"), os.getenv("NEO4J_PASSWORD"))
        )

    def close(self):
        self.driver.close()

    def execute_query(self, query, params=None):
        with self.driver.session() as session:
            result = session.run(query, params or {})
            return result

    def create_user(self, username, password):
        # hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # create the user node in Neo4j
        query = """
        CREATE (u:User {username: $username, password: $password})
        RETURN u
        """
        params = {"username": username, "password": hashed_password.decode('utf-8')}
        result = self.execute_query(query, params)
        return result.single()

    def validate_user(self, username, password):
        # Find user by username
        query = """
        MATCH (u:User {username: $username})
        RETURN u.password AS stored_password
        """
        params = {"username": username}
        result = self.execute_query(query, params)
        
        if result.peek():
            stored_password = result.single()["stored_password"]
            # check if the entered password matches the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
                return True
        return False
