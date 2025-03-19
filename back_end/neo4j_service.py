from neo4j import GraphDatabase
import os
from dotenv import load_dotenv
import bcrypt
import json
import datetime

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
        
    # Purpose    : returns all trees in database
    # Parameters : none
    # Returns    : list of all tree names (string)
    def get_tree_list(self):
        with self.driver.session() as session:
            result = session.run("MATCH (t:Tree) RETURN t.name AS tree_name")
            return [record["tree_name"] for record in result]
    
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
            record = session.run(query, username = username,
                                  password = hashed_password.decode('utf-8')).single()
            return json.dumps({"username" : record["username"] if record
                                else None, "status_code" : 201})
        
    # Purpose    : delete a user from the neo4j instance and all of the
    #              associated trees and tree data
    # Parameters : username (string) - username of user to be removed
    #              password (string) - password of user to be removed
    # Returns    : a json string with the number of users deleted (or None
    #              if this failed) and the associated HTTP response status code
    #              (format: {"deleted_count" : 1, "status_code" : 200})
    def remove_user(self, username, password):

        valid_user = json.loads(self.__verify_credentials(username, password))

        if not valid_user["valid"]:
            return json.dumps({"deleted_count" : 0, 
                               "status_code" : valid_user["status_code"]})

        # delete the user if the password is correct
        delete_query = """
        MATCH (u:User {username: $username}) 
        OPTIONAL MATCH (u)-[:HAS_TREE]->(t:Tree) 
        DETACH DELETE t, u 
        RETURN COUNT(u) AS deleted_count
        """
        
        with self.driver.session() as session:
            record = session.run(delete_query, username = username).single()
            return json.dumps({"deleted_count" : record["deleted_count"] 
                               if record else 0, "status_code" : 200})

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
        if not bcrypt.checkpw(password.encode('utf-8'), 
                              stored_hashed_password.encode('utf-8')):
            return json.dumps({"valid" : False, "status_code" : 401})
        
        return json.dumps({"valid" : True, "status_code" : 200})
    
    # Purpose    : determines whether user exists
    # Parameters : username (string) - username of user to be verified
    # Returns    : a json string with a boolean of whether the user exists 
    #              and the associated HTTP response status code
    #              (format: {"valid" : True, "status_code" : 200})
    def __verify_user_exists(self, username):
        query = """
        MATCH (u:User {username: $username})
        RETURN u
        """

        # check if user exists
        with self.driver.session() as session:
            record = session.run(query, username = username).single()
            if record:
                return json.dumps({"valid" : True, "status_code" : 200})
            else:
                return json.dumps({"valid" : False, "status_code" : 404})
            
    # Purpose    : determines whether a tree exists
    # Parameters : username (string)  - username of user whose tree is to be
    #              verified
    #              tree_name (string) - name of tree to be verified
    # Returns    : a boolean of whether the tree exists
    def __tree_exists(self, username, tree_name):
        query = """
        MATCH (u:User {username: $username}) -[:HAS_TREE]-> (t:Tree {name: $tree_name})
        RETURN t
        """

        # check if user exists
        with self.driver.session() as session:
            record = session.run(query, username = username, 
                                 tree_name = tree_name).single()
            if record:
                return True
            else:
                return False
            
    
    # Purpose    : get all trees a specific user has
    # Parameters : username (string)  - username of user whose trees we want
    #              to retrieve
    # Returns    : a json string with a string array containing the names of 
    #              all treees belonging to this user, None if the query failed,
    #              or an empty array if the user has no trees and the
    #              associated HTTP response status code
    #              (format: {"trees" : ["tree1", "tree2"], "status_code" : 200})
    def get_trees(self, username):

        # make sure user exists
        if json.loads(self.__verify_user_exists(username))["valid"]:
            # get trees connected to user
            get_trees_query = """
            MATCH (u:User {username: $username})-[r:HAS_TREE]->(t:Tree)
            RETURN t.name AS tree_names
            ORDER BY r.last_opened DESC
            """

            with self.driver.session() as session:
                result = session.run(get_trees_query, username = username)
                tree_names = [record["tree_names"] for record in result]
                return json.dumps({"tree_names" : tree_names, "status_code" : 200})
            
        else:
            return json.dumps({"tree_names" : None, "status_code" : 404})

    # Purpose    : add a tree to the neo4j instance
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of the tree to be added
    # Returns    : a json string with the name of the tree added (or None if
    #              failed) and the associated HTTP response status code
    #              (format: {"tree_name" : "family name", "status_code" : 201})
    def add_tree(self, username, tree_name):

        if self.__tree_exists(username, tree_name):
            return json.dumps({"tree_name": None, "status_code": 409})

        # add tree connected to user
        add_tree_query = """
        MATCH (u:User {username: $username})
        CREATE (t:Tree {name: $tree_name})
        CREATE (u)-[:HAS_TREE {last_opened: $date}]->(t)
        RETURN t.name AS tree_name
        """

        with self.driver.session() as session:
            record = session.run(add_tree_query, username = username,
                                  tree_name = tree_name, date = datetime.datetime.now()).single()
            return json.dumps({"tree_name" : record["tree_name"] if record
                                else None, "status_code" : 201 if record
                                else 500})

    # Purpose    : remove a tree from the neo4j instance
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of the tree to be removed
    # Returns    : a json string with the name of the tree removed (or None if
    #              failed) and the associated HTTP response status code
    #              (format: {"tree_name" : "family name", "status_code" : 201})
    def remove_tree(self, username, tree_name):

        # add tree connected to user
        remove_tree_query = """
        MATCH (u:User {username: $username})-[:HAS_TREE]->(t:Tree {name: $tree_name})
        DETACH DELETE t
        RETURN Count(t) AS deleted_trees
        """

        with self.driver.session() as session:
            record = session.run(remove_tree_query, username = username,
                                  tree_name = tree_name).single()
            print("COUNT")
            print(record["deleted_trees"])
            return json.dumps({"deleted_trees" : record["deleted_trees"] if record
                                else 0, "status_code" : 200 if (record["deleted_trees"] > 0)
                                else 500})
        
    # Purpose    : set the last opened date of a tree to now
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of the tree to be updated
    # Returns    : a json string with the last opened date of the tree (or None
    #              if failed) and the associated HTTP response status code
    #              (format: {"last_opened" : "2021-01-01T00:00:00.000Z",
    #  "status_code" : 200})
    def set_last_opened_tree(self, username, tree_name):
        query = """
        MATCH (:User {username: $username})-[r:HAS_TREE]->(:Tree {name: $tree_name})
        SET r.last_opened = $date
        RETURN r.last_opened AS last_opened
        """

        with self.driver.session() as session:
            record = session.run(query, username = username, tree_name = tree_name,
                                 date = datetime.datetime.now()).single()
            return json.dumps({"last_opened" : 
                               record["last_opened"].strftime("%Y-%m-%d %H:%M:%S") 
                               if record else None, "status_code" : 200 if record
                                else 500})

