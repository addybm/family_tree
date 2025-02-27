from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import bcrypt
import json

class Neo4jService:

    # Purpose    : initialize the Neo4j service object with the env variable
    #              credentials
    # Parameters : none
    # Returns    : none
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

    # Purpose    : retrieves all usernames from neo4j instance
    # Parameters : none
    # Returns    : list of all usernames (strings)
    def get_users(self):
        with self.driver.session() as session:
            result = session.run("MATCH (u:User) RETURN u.username AS username")
            return [record["username"] for record in result]
    
    # Purpose    : add a user to the neo4j instance
    # Parameters : username (string) - username of user to be added
    #              password (string) - password of user to be added
    # Returns    : a json string with the username of the added user (or None
    #              if not added) and the associated HTTP response status code
    #              (format: {"username" : "a_user", "status_code" : 200})
    def create_user(self, username, password):

        # check that password is >= 8 characters
        if len(password) < 8:
            return json.dumps({"username" : None, "status_code" : 400})

        # hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # check if the username already exists
        check_query = """
        MATCH (u:User {username: $username})
        RETURN u
        """

        with self.driver.session() as session:
            existing_user = session.run(check_query, username = username).single()
            if existing_user:
                return json.dumps({"username" : None, "status_code" : 409})
        
        # create the user node in Neo4j
        query = """
        CREATE (u:User {username: $username, password: $password})
        RETURN u.username AS username
        """

        with self.driver.session() as session:
            record = session.run(query, username = username, password = hashed_password.decode('utf-8')).single()
            return json.dumps({"username" : record["username"] if record else None, "status_code" : 201})
        
    # Purpose    : delete a user from the neo4j instance
    # Parameters : username (string) - username of user to be removed
    #              password (string) - password of user to be removed
    # Returns    : a json string with the number of users deleted (or None
    #              if this failed) and the associated HTTP response status code
    #              (format: {"deleted_count" : 1, "status_code" : 200})
    def remove_user(self, username, password):

        valid_user = json.loads(self.__verify_credentials(username, password))

        if not valid_user["valid"]:
            return json.dumps({"deleted_count" : 0, "status_code" : valid_user["status_code"]})

        # delete the user if the password is correct
        delete_query = """
        MATCH (u:User {username: $username})
        DELETE u
        RETURN COUNT(u) AS deleted_count
        """
        
        with self.driver.session() as session:
            record = session.run(delete_query, username = username).single()
            return json.dumps({"deleted_count" : record["deleted_count"] if record else 0, "status_code" : 200})

    # Purpose    : determines whether provided credentials are valid
    # Parameters : username (string) - username of user to be verified
    #              password (string) - password of user to be verified
    # Returns    : a json string with a boolean of whether the credentials are
    #              valid and the associated HTTP response status code
    #              (format: {"valid" : True, "status_code" : 200})
    def login(self, username, password):
        return self.__verify_credentials(username, password)
    
    # Purpose    : determines whether provided credentials are valid
    # Parameters : username (string) - username of user to be verified
    #              password (string) - password of user to be verified
    # Returns    : a json string with a boolean of whether the credentials are
    #              valid and the associated HTTP response status code
    #              (format: {"valid" : True, "status_code" : 200})
    def __verify_credentials(self, username, password):
        query = """
        MATCH (u:User {username: $username})
        RETURN u.password AS password
        """

        # check if user exists
        with self.driver.session() as session:
            record = session.run(query, username = username).single()
            if not record:
                return json.dumps({"valid" : False, "status_code" : 404})
            
            stored_hashed_password = record["password"]
        
        # check if password is correct
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
            return json.dumps({"valid" : False, "status_code" : 401})
        
        return json.dumps({"valid" : True, "status_code" : 200})
