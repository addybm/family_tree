from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import bcrypt

class Neo4jService:

    def __init__(self):
        # Load environment variables
        load_dotenv()

        NEO4J_URI = os.getenv("NEO4J_URI")
        NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
        NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

        if not NEO4J_URI or not NEO4J_USERNAME or not NEO4J_PASSWORD:
            raise ValueError("NEO4J environment variables are not set correctly")

        self.driver = GraphDatabase.driver(
            NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
        )

    def get_users(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u.username AS username")
            return [record["username"] for record in result]
    
    def create_user(self, username, password):
        # hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        
        # create the user node in Neo4j
        query = """
        CREATE (u:User {username: $username, password: $password})
        RETURN u.username AS username
        """

        with self.driver.session() as session:
            result = session.run(query, username = username, password = hashed_password.decode('utf-8'))
            record = result.single()
            # print("RETURNING: " + record["username"])
            return record["username"] if record else None


# class Neo4jService:
    # def __init__(self):
    #     NEO4J_URI = os.getenv("NEO4J_URI")
    #     NEO4J_USERNAME = os.getenv("NEO4J_USERNAME")
    #     NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

    #     if not NEO4J_URI or not NEO4J_USERNAME or not NEO4J_PASSWORD:
    #         raise ValueError("NEO4J environment variables are not set correctly")

    #     self.driver = GraphDatabase.driver(
    #         NEO4J_URI, auth=(NEO4J_USERNAME, NEO4J_PASSWORD)
    #     )

#     def close(self):
#         self.driver.close()

#     def execute_query(self, query, params=None):
#         with self.driver.session() as session:
#             result = session.run(query, params or {})
#             return result


    # def create_user(self, username, password):
    #     """Creates a new user in Neo4j with a hashed password and returns the full node."""
    #     hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    #     query = """
    #     CREATE (u:User {username: $username, password: $password})
    #     RETURN u
    #     """

    #     with self.driver.session() as session:
    #         result = session.run(query, username=username, password=hashed_password)
    #         record = result.single()
    #         return record["u"] if record else None



    # def validate_user(self, username, password):
    #     # Find user by username
    #     query = """
    #     MATCH (u:User {username: $username})
    #     RETURN u.password AS stored_password
    #     """
    #     params = {"username": username}
    #     result = self.execute_query(query, params)
        
    #     if result.peek():
    #         stored_password = result.single()["stored_password"]
    #         # check if the entered password matches the stored hash
    #         if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):
    #             return True
    #     return False
