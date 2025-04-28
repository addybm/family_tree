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

    # Purpose    : sends query to database
    # Parameters : query (string) - the query to be sent to the database
    # Returns    : a list of records returned by the query
    def send_query(self, query):
        with self.driver.session() as session:
            result = session.run(query)
            return [record for record in result]

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
        
    # Purpose    : returns all people in database
    # Parameters : none
    # Returns    : list of all people names (string)
    def get_people_list(self):
        with self.driver.session() as session:
            result = session.run("MATCH (p:Person) RETURN p.name AS person_name")
            return [record["person_name"] for record in result]
    
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
        OPTIONAL MATCH (t)-[:HAS_PERSON]->(p:Person)
        DETACH DELETE p, t, u 
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
        OPTIONAL MATCH (t)-[r:HAS_PERSON]->(p:Person)
        DETACH DELETE p, t
        RETURN COUNT(t) AS deleted_trees
        """

        with self.driver.session() as session:
            record = session.run(remove_tree_query, username = username,
                                  tree_name = tree_name).single()
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
    
    # Purpose    : add the first person to a tree and set them as the focus
    # Parameters : username (string)  - username of user whose tree it is
    #              person (Person)   - the person to be added
    #              tree_name (string) - name of the tree to be updated
    # Returns    : a json string with the name of the person added (or None
    #              if failed) and the associated HTTP response status code
    #              (format: {"person_name" : "John Doe", "status_code" : 200})
    def add_person(self, username, person, tree_name):
        query = """
        MATCH (u:User {username: $username})-[r:HAS_TREE]->(t:Tree {name: $tree_name})
        CREATE (p:Person {name: $name, gender: $gender, nickname: $nickname, notes: $notes})
        CREATE (t)-[:HAS_PERSON]->(p)
        CREATE (t)-[:IN_FOCUS]->(p)
        RETURN p.name AS person_name
        """

        with self.driver.session() as session:
            record = session.run(query, username = username,
                                 tree_name = tree_name, name = person["name"],
                                   gender = person["gender"],
                                     nickname = person["nickname"],
                                       notes = person["notes"]).single()
            return json.dumps({"person_name" : record["person_name"] if record
                                else None, "status_code" : 200 if record
                                else 500})
        
    
    # Purpose    : gets the in_focus person of a tree
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of the tree to be checked
    # Returns    : a json string with the JSON-version of the person object
    #              in focus (or None if no person) and the associated HTTP 
    #              response status code
    #              ({"person": {"name" : "person", "gender" : "male", 
    #                "nickname" : "nick", "notes" : "notes"}}, 200)
    def get_focus(self, username, tree_name):
        query = """
        MATCH (u:User {username: $username})-[r:HAS_TREE]->(t:Tree {name: $tree_name})
        OPTIONAL MATCH (t)-[:IN_FOCUS]->(p:Person)
        RETURN p.name AS person_name, p.gender AS person_gender, p.nickname AS person_nickname, p.notes AS person_notes
        """

        with self.driver.session() as session:
            record = session.run(query, username = username, tree_name = tree_name).single()
            if record["person_name"] and record["person_gender"] and record["person_nickname"] and record["person_notes"]:
                person = {"name": record["person_name"], 
                          "gender": record["person_gender"],
                          "nickname": record["person_nickname"],
                          "notes": record["person_notes"]}
                return json.dumps({"person" : person, "status_code" : 200})
            else:
                return json.dumps({"person" : None, "status_code" : 200})

    # Purpose    : set the focus of a tree to a specific person
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of the tree to be updated
    #              person_name (string) - name of the person to be set as focus
    # Returns    : a json string with the name of the person set as focus (or None
    #              if failed) and the associated HTTP response status code
    #              (format: {"person_name" : "John Doe", "status_code" : 200})
    # def set_focus(self, username, tree_name, person_name):
    #     query = """
    #     MATCH (u:User {username: $username})-[r:HAS_TREE]->(t:Tree {name: $tree_name})
    #     MATCH (p:Person {name: $person_name})
    #     MERGE (t)-[:IN_FOCUS]->(p)
    #     RETURN p.name AS person_name
    #     """

    #     with self.driver.session() as session:
    #         record = session.run(query, username = username, tree_name = tree_name,
    #                              person_name = person_name).single()
    #         return json.dumps({"person_name" : record["person_name"] if record
    #                             else None, "status_code" : 200 if record
    #                             else 500})


    # Purpose    : delete the person who is in focus
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of the tree to be updated
    # Returns    : a json string with the number of people deleted (or None if
    #              failed) and the associated HTTP response status code
    #              (format: {"deleted_count" : 1, "status_code" : 200})
    def delete_person(self, username, tree_name):
        query = """
        MATCH (u:User {username: $username}) -[:HAS_TREE]-> (t:Tree {name: $tree_name})
        MATCH (t)-[:IN_FOCUS]->(p:Person)
        DETACH DELETE p
        RETURN COUNT(p) AS deleted_count
        """

        with self.driver.session() as session:
            record = session.run(query, username = username, tree_name = tree_name).single()
            return json.dumps({"deleted_count" : record["deleted_count"] if record
                                else None, "status_code" : 200 if record
                                else 500})
        
    # Purpose    : adds a parent to the in-focus person in the tree
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of tree to be modified
    #              parent (dict)      - dictionary matching the Person class
    #              definition
    # Returns    : a json string with the parent name and an associated HTTP
    #              status code
    def add_parent(self, username, tree_name, parent):
        query = """
        MATCH (u:User {username: $username}) -[:HAS_TREE]-> (t:Tree {name: $tree_name})
        MATCH (t)-[:IN_FOCUS]->(child:Person)
        CREATE (parent:Person {name: $name, gender: $gender, nickname: $nickname, notes: $notes})
        CREATE (child)-[:HAS_PARENT]->(parent)
        CREATE (parent)-[:HAS_CHILD]->(child)
        CREATE (t)-[:HAS_PERSON]->(parent)
        RETURN parent.name AS parent_name
        """

        with self.driver.session() as session:
            record = session.run(query, username = username,
                                  tree_name = tree_name,
                                    name = parent["name"],
                                      gender = parent["gender"],
                                        nickname = parent["nickname"],
                                          notes = parent["notes"]).single()
            return json.dumps({"parent_name" : record["parent_name"] if record
                                else None, "status_code" : 200 if record
                                else 500})
    
    # TODO
    def __format_spacing(self, tree):
        return {}
    
    # parse record and call other functions
    # TODO: write this docstring more nicely
    # record is a dictionary of arrays containing all of the fields we've retrieved
    def __add_relationships(self, person, queue, tree, marriages, divorces, children, record):
        self.__add_parents(person, queue, tree, children, record["parents"])
        # self.__add_partners(person, queue, tree, marriages, record["partners"])
        # self.__add_ex_partners(person, queue, tree, divorces, record["ex_partners"])
        # self.__add_children(person, queue, tree, children, record["children"])
        return
    
    #TODO: make function contract better
    # Purpose    : adds a parent to the relationships, queue, and tree
    # Parameters : queue (array of dictionaries)   - the nodes left to explore
    #              in the current tree
    #              tree (dictionary of arrays)     - the respresentation of the
    #              currently-fetched tree
    #              parents (array of dictionaries) - array of dictionaries with
    #              the keys: name, gender, nickname, notes, and id
    # Returns    : none (queue and tree will be modified directly)
    def __add_parents(self, person, queue, tree, children, parents):

        num_parents = len(parents)
        if num_parents > 1:
            parents = sorted(parents, key=lambda p: p["name"].lower())

            parent_one = parents[0]["name"]
            parent_two = parents[1]["name"]

        elif num_parents == 1:
            parent_one = parents[0]["name"]
            parent_two = parents[0]["name"]
        else:
            return

        # if these parents are already listed, skip
        for pair in children:
            if (pair[0] == parent_one and pair[1] == parent_two
                ) or (pair[0] == parent_two and pair[1] == parent_one):
                return
            
        # add to queue alphabetically
        queue.append({"person": {"name" : parents[0]["name"], 
                                 "gender" : parents[0]["gender"],
                                   "nickname" : parents[0]["nickname"],
                                   "notes" : parents[0]["notes"]}, 
                      "id" : parents[0]["id"], "in-focus": False})
        if num_parents > 1:
            queue.append({"person": {"name" : parents[1]["name"], 
                            "gender" : parents[1]["gender"],
                            "nickname" : parents[1]["nickname"],
                            "notes" : parents[1]["notes"]}, 
                "id" : parents[1]["id"], "in-focus" : False})

        # add both parents to the "children" relationships with "person" as 
            # their child (alphabetically by first name if 2 parents)
        children.append([parent_one, parent_two, person["person"]["name"]])
        # TODO: think about this, "children" feels a little messy

        # add both parents to the tree (alphabetically by first name, above
            # their children)
        
        row_parents = None
        idx_parents = None
        for key, people in tree.items():
            for index, node in enumerate(people):
                row_parents = str(int(key) - 1)
                if node["person"]["name"] == person["person"]["name"]:
                    self.__add_parents_tree(tree, row_parents, idx_parents, parents)
                    return
                else:
                    # move parent counters if applicable
                    idx_parents = self.__check_parents(tree, node, children, row_parents, idx_parents)
        return
    
    # Purpose    : adds parents to the tree
    # TODO: improve
    def __add_parents_tree(self, tree, row_parents, idx_parents, parents):
        # add the parents if in-bounds, otherwise creates new first row
        if (row_parents == "-1"):
            idx = max(int(k) for k in tree.keys())
            while idx > 0:
                if str(idx - 1) in tree:
                    tree[str(idx)] = tree[str(idx - 1)]
                else:
                    tree[str(idx)] = {}
                    tree[str(idx - 1)] = {}
            tree["0"] = [{"person" : {"name" : parent["name"], 
                                      "gender" : parent["gender"], 
                                      "nickname" : parent["nickname"], 
                                      "notes" : parent["notes"]}, 
                                      "id" : parent["id"], 
                                      "in-focus" : False} 
                                      for parent in parents]
        
        # tree[row_parents].insert(parents[0],idx_parents)
        if row_parents in tree:
            tree[row_parents].insert({"person": {"name" : parents[0]["name"], 
                                 "gender" : parents[0]["gender"],
                                   "nickname" : parents[0]["nickname"],
                                   "notes" : parents[0]["notes"]}, 
                                   "id" : parents[0]["id"], 
                                   "in-focus": False}
                                   ,idx_parents)
            if len(parents) > 1:
                tree[row_parents].insert({"person": {"name" : parents[1]["name"], 
                                 "gender" : parents[1]["gender"],
                                   "nickname" : parents[1]["nickname"],
                                   "notes" : parents[1]["notes"]}, 
                                   "id" : parents[1]["id"], 
                                   "in-focus": False}
                                   ,idx_parents + 1)
        else:
            tree[row_parents] = [{"person" : {"name" : parent["name"], 
                                      "gender" : parent["gender"], 
                                      "nickname" : parent["nickname"], 
                                      "notes" : parent["notes"]}, 
                                      "id" : parent["id"], 
                                      "in-focus" : False} 
                                      for parent in parents]

        return

    # check whether someone's parents are in the tree and adjust where new
    # parents should be placed accordingly
    def __check_parents(self, tree, node, children, row_parents, idx_parents):
        # are their parents listed in "children"
        for relationship in children:
            if node["person"]["name"] in relationship:
                parent_one = relationship[0]
                parent_two = relationship[1]
                # do they match the next 1/2 people in the position [row_parents][idx_parents] (might be out of bounds)
                if (parent_one == tree[row_parents][idx_parents]["person"]["name"]):
                    idx_parents += 1
                    if (parent_two == tree[row_parents][idx_parents]["person"]["name"]):
                        idx_parents += 1
        return idx_parents
    
    def __add_partners(self, queue, tree):
        return

    def __add_ex_partners(self, queue, tree):
        return

    def __add_children(self, queue, tree):
        return


    # Purpose    : gets a correctly-formatted respresentation of a tree
    # Parameters : username (string)  - username of user whose tree it is
    #              tree_name (string) - name of tree to be modified
    #              max_height (int)  - maximum height of tree (number of total 
    #                                  generations to get)
    #              max_width (int)   - maximum width of tree (maximum number of 
    #                                  total people that can be shown per row in
    #                                  the tree)
    #              initial_focus_row - the row (with the top row being 0) where 
    #                                  the in-focus person should be, if possible
    #               example: if someone inputs 0, they should be started at row
    #               zero, but if there is no information above them but 2 
    #               generations below them, they will be moved to row 1 assuming
    #               the max_height allows for it
    # Returns    : a json string with the tree (in the form of a dictionary of 
    #              arrays where each key is a row of a tree and each array is 
    #              made up of dictionaries containing a person : Person, 
    #              id : string, and in_focus : boolean) and an associated HTTP
    #              status code
    def get_tree(self, username, tree_name, max_height, max_width, initial_focus_row):

        # - If adding missing information:
        #    - {missing_parents, missing_partner_left, missing_partner_right, missing_children}

        queue = []
        tree = {}
        marriages = []
        divorces = []
        children = []

        # get in-focus node and add to the queue and tree
        query = """
            MATCH (u:User {username: $username}) -[:HAS_TREE]-> 
                (t:Tree {name: $tree_name})
            MATCH (t) -[IN_FOCUS]->(p:Person)
            RETURN p.name AS name, p.gender AS gender, p.nickname AS nickname,
                p.notes AS notes, elementId(p) AS id
            """
        
        # TODO: getting a warning about the following code that I'm unable to fix
        with self.driver.session() as session:
            record = session.run(query, username = username,
                                  tree_name = tree_name).single()
            if record:
                queue.append({"person" : {"name" : record["name"],
                                          "gender" : record["gender"],
                                          "nickname" : record["nickname"],
                                          "notes" : record["notes"]},
                                          "id": record["id"],
                                          "in_focus": True})
                #TODO: should this key be a string?
                tree[initial_focus_row] = [{"person": {"name" : record["name"],
                                          "gender" : record["gender"],
                                          "nickname" : record["nickname"],
                                          "notes" : record["notes"]},
                                          "id": record["id"],
                                          "in_focus": True}]
            else:
                return json.dumps({"tree": {}, "status_code": 500})
        
        
            while not len(queue) == 0:

                # pop the first element from the queue (0)
                person = queue.pop(0)

                # get partners, parents, and children and add to the queue and tree
                # if space
                # add as missing if no space

                query = """
                    MATCH (p)
                    WHERE elementId(p) = $id
                    OPTIONAL MATCH (p)-[:HAS_PARENT]->(parents:Person)
                    OPTIONAL MATCH (p)-[:PARTNER]->(partner:Person)
                    OPTIONAL MATCH (p)-[:EX_PARTNER]->(ex_partners:Person)
                    OPTIONAL MATCH (p)-[:HAS_CHILD]->(children:Person)
                    RETURN
                    [
                        p IN COLLECT(parents) WHERE p IS NOT NULL |
                        {
                            name: p.name,
                            gender: p.gender,
                            nickname: p.nickname,
                            notes: p.notes,
                            id: elementId(p)
                        }
                    ] AS parents,
                    [
                        p IN COLLECT(partner) WHERE p IS NOT NULL |
                        {
                            name: p.name,
                            gender: p.gender,
                            nickname: p.nickname,
                            notes: p.notes,
                            id: elementId(p)
                        }
                    ] AS partners,
                    [
                        p IN COLLECT(ex_partners) WHERE p IS NOT NULL |
                        {
                            name: p.name,
                            gender: p.gender,
                            nickname: p.nickname,
                            notes: p.notes,
                            id: elementId(p)
                        }
                    ] AS ex_partners,
                    [
                        c IN COLLECT(children) WHERE c IS NOT NULL |
                        {
                            name: c.name,
                            gender: c.gender,
                            nickname: c.nickname,
                            notes: c.notes,
                            id: elementId(c)
                        }
                    ] AS children
                    """
                
                # with self.driver.session() as session:
                record_second = list(session.run(query, id = person["id"]))[0]
                if record_second:
                    self.__add_relationships(person, queue, tree, marriages,
                                            divorces, children, record_second)
                else:
                    return json.dumps({"tree": {}, "status_code": 500})
                

        # TODO: modify tree spacing (create a function)
        self.__format_spacing(tree)

        # TODO: change status code so it reflects something real
        return json.dumps({"tree": tree, "status_code": 200})
    


