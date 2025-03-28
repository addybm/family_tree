from flask import Flask, jsonify, request
from flask_cors import CORS
import atexit
from neo4j_service import Neo4jService
import json
from Person import Person


app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for React)
neo_service = Neo4jService()

# Purpose    : retrieves all usernames from neo4j instance
# Parameters : none
# Returns    : json string of all usernames (strings)
@app.route('/data', methods = ["GET"])
def data():
    users = neo_service.get_users()
    trees = neo_service.get_tree_list()
    people = neo_service.get_people_list()
    return jsonify({'users' : users, 'trees' : trees, 'people' : people})

# Purpose    : sends a query to the neo4j instance
# Parameters : none (retrieves from a posted json, which should have:
#              query (string) - query to be sent to the neo4j instance)
# Returns    : none
@app.route('/api/query', methods = ["POST"])
def send_query():
    data = request.get_json()
    query = data.get("query")
    if query:
        result = neo_service.send_query(query)
        return jsonify(result), 200
    else:
        return jsonify({"message": "Query required"}), 400

# Purpose    : adds a user to the neo4j instance
# Parameters : none (retrieves from a posted json, which should have:
#              username (string) - username of user to be removed
#              password (string) - password of user to be removed)
# Returns    : a tuple containing a json string with a message saying whether
#              or not a user was removed successfully and the username of the
#              user we're trying to add, as well as an HTTP status code
#              ({"message" : "User removed successfully", "user" : "testuser"},
#                200)
@app.route('/api/register', methods = ["POST"])
def register_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        result = json.loads(neo_service.create_user(username, password))
        if result["username"]:
            return jsonify({"message": "User registered successfully", "user": result["username"]}), result["status_code"]
        else:
            return jsonify({"message": "User not registered successfully", "user": username}), result["status_code"]
    else:
        return jsonify({"message": "Username and password required", "user" : username if username else None}), 400

# Purpose    : delete a user from the neo4j instance
# Parameters : none (retrieves from a posted json, which should have:
#              username (string) - username of user to be removed
#              password (string) - password of user to be removed)
# Returns    : a tuple containing a json string with a message saying whether
#              or not a user was removed successfully, as well as an HTTP
#              status code
#              ({"message" : "User removed successfully"}, 200)
@app.route('/api/remove', methods = ["POST"])
def remove_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        result = json.loads(neo_service.remove_user(username, password))
        # if we deleted 1 or more accounts successfully
        if result["deleted_count"] > 0:
            return jsonify({"message": "User removed successfully"}), result["status_code"]
        else:
            return jsonify({"message": "User not removed"}), result["status_code"]
    else:
        return jsonify({"message": "Existing username and password required"}), 400

# Purpose    : checks a users credentials in the neo4j instance
# Parameters : none (retrieves from a posted json, which should have:
#              username (string) - username of user to be removed
#              password (string) - password of user to be removed)
# Returns    : a tuple containing a json string with a message saying whether
#              or not a user was verified successfully, as well as an HTTP
#              status code
#              ({"message" : "User credentials valid"}, 200)
@app.route('/api/login', methods = ["POST"])
def login_user():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if username and password:
        result = json.loads(neo_service.login(username, password))
        if result["valid"]:
            return jsonify({"message": "User credentials valid"}), result["status_code"]
        else:
            return jsonify({"message": "User credentials invalid"}), result["status_code"]
    else:
        return jsonify({"message": "Existing username and password required"}), 400
    

# Purpose    : gets a list of tree names created by a given user
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose trees we want
# Returns    : a tuple containing a json string with a list of this user's
#              trees, as well as an HTTP status code
#              ({"tree_names" : ["tree1", "tree2"]}, 200)
@app.route('/api/trees', methods = ["GET"])
def get_trees():
    username = request.args.get("username")

    if username:
        result = json.loads(neo_service.get_trees(username))
        if result["tree_names"] is not None:
            return jsonify({"tree_names": result["tree_names"]}), result["status_code"]
        else:
            return jsonify({"tree_names": None}), result["status_code"]
    else:
        return jsonify({"tree_names": None}), 400

# Purpose    : adds a new tree to the array of user trees
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be added)
# Returns    : a tuple containing a json string with a message saying whether
#              or not the tree was added successfully, as well as an HTTP
#              status code
#              ({"message" : "Tree added"}, 201)
@app.route('/api/add_tree', methods = ["POST"])
def add_tree():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")

    if username and tree_name:
        result = json.loads(neo_service.add_tree(username, tree_name))
        if result["tree_name"] is not None:
            return jsonify({"message": "Success: tree: " + result["tree_name"]
                             + " created"}), result["status_code"]
        else:
            return jsonify({"message": "Error: tree not created"}), result["status_code"]
    else:
        return jsonify({"message": "Username and tree name required"}), 400
    
# Purpose    : removes a new tree from the array of user trees
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be removed)
# Returns    : a tuple containing a json string with a message saying whether
#              or not the tree was removed successfully, as well as an HTTP
#              status code
#              ({"message" : "Tree removed"}, 200)
@app.route('/api/remove_tree', methods = ["POST"])
def remove_tree():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")

    if username and tree_name:
        result = json.loads(neo_service.remove_tree(username, tree_name))
        if result["deleted_trees"] > 0:
            return jsonify({"message": "Success: " + 
                            str(result["deleted_trees"]) + 
                            " tree(s) removed"}), result["status_code"]
        else:
            return jsonify({"message": 
                            "Error: tree not removed"}), result["status_code"]
    else:
        return jsonify({"message": "Username and tree name required"}), 400

# Purpose    : modifies the last opened tree of a user
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be set as last opened)
# Returns    : a tuple containing a json string with a message saying whether
#              or not the tree was modified successfully, as well as an HTTP
#              status code
#              ({"message" : "Success: last opened tree: tree1 modified"}, 200)
@app.route('/api/modify_last_opened', methods = ["POST"])
def modify_last_opened_tree():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")

    if username and tree_name:
        result = json.loads(neo_service.set_last_opened_tree(username, tree_name))
        if result["last_opened"] is not None:
            return jsonify({"message": "Success: last opened tree: " + tree_name
                            + " " + " on " + result["last_opened"]}), result["status_code"]
        else:
            return jsonify({"message": "Error: tree not modified"}), result["status_code"]

if __name__ == '__main__':
    app.run(debug = True, port = 5002)

# Purpose    : closes the neo4j connection when the program exits
# Parameters : none
# Returns    : none
# def close_neo4j_connection():
#     neo_service.close()
# atexit.register(close_neo4j_connection)

# Purpose    : adds the first person to a tree and sets the focus
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              person (Person)    - Person to add
#              tree_name (string) - name of tree to be modified
# Returns    : a tuple containing a json string with a message saying whether
#              or not the person was added successfully, as well as an HTTP
#              status code
#              ({"message" : "Success: person added"}, 200)
#              ({"message" : "Error: person not created"}, 400)
@app.route('/api/add_person', methods = ["POST"])
def add_person():
    data = request.get_json()
    username = data.get("username")
    person = data.get("person")
    tree_name = data.get("tree_name")

    if person and tree_name:
        result = json.loads(neo_service.add_person(username, person, tree_name))
        if result["person_name"] is not None:
            return jsonify({"message": "Success: person added"}), result["status_code"]
        else:
            return jsonify({"message": "Error: person not created"}), result["status_code"]
    else:
        return jsonify({"message": "Person and tree name required"}), 400

# Purpose    : changes the in-focus person of a tree
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username to be in focus
#              tree_name (string) - name of tree to be modified
#              person_name (string) - name of person to be in focus)
# Returns    : a tuple containing a json string with a message saying whether
#              or not the in-focus person was modified successfully, as well as
#              an HTTP status code
#              ({"message" : "Success: focus changed"}, 200)
#              ({"message" : "Error: focus not modified"}, 400)
# @app.route('/api/modify_in_focus', methods = ["POST"])
# def change_focus():
#     data = request.get_json()
#     username = data.get("username")
#     tree_name = data.get("tree_name")
#     person_name = data.get("person_name")
#     if username and tree_name and person_name:
#         result = json.loads(neo_service.set_focus(username, tree_name, person_name))
#         if result["focus"] is not None:
#             return jsonify({"message": "Success: focus changed"}), result["status_code"]
#         else:
#             return jsonify({"message": "Error: focus not modified"}), result["status_code"]
#     else:
#         return jsonify({"message": "Username, tree name and person name required"}), 400
    

# Purpose    : gets the in-focus person of a tree
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be investigated)
# Returns    : a tuple containing a json string with a dictionary of the
#              in-focus person, as well as an HTTP status code
#              ({"person": {"name" : "person", "gender" : "male", 
#                "nickname" : "nick", "notes" : "notes"}}, 200)
@app.route('/api/get_in_focus', methods = ["GET"])
def get_focus():
    username = request.args.get("username")
    tree_name = request.args.get("tree_name")
    if username and tree_name:
        result = json.loads(neo_service.get_focus(username, tree_name))
        # if result["person"] is not None:
        #     return jsonify({"person": result["person"]}), result["status_code"]
        # else:
        #     return jsonify({"person": {}}), result["status_code"]
        return jsonify({"person": result["person"]}), result["status_code"]
    else:
        return jsonify({"person": None}), 400
    

# Purpose    : deletes the in-focus person from a tree
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be modified)
# Returns    : a tuple containing a json string with a message saying whether
#              or not the in-focus person was deleted successfully, as well as
#              an HTTP status code
#              ({"message" : "Success: person deleted"}, 200)
@app.route('/api/delete_person', methods = ["POST"])
def delete_person():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")

    if username and tree_name:
        result = json.loads(neo_service.delete_person(username, tree_name))
        if result["deleted_count"] > 0:
            return jsonify({"message": "Success: person deleted"}), result["status_code"]
        else:
            return jsonify({"message": "Error: person not deleted"}), 400
    else:
        return jsonify({"message": "Username and tree name required"}), 400
    

# Purpose    : adds a parent to the in-focus person in the tree
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be modified
#              parent (dict)      - dictionary matching the Person class
#              definition
# Returns    : a tuple containing a json string with a message saying whether
#              or not the parent was added successfully, as well as an HTTP
#              status code
#              ({"message" : "Success: parent added"}, 200)
@app.route('/api/add_parent', methods = ["POST"])
def add_parent():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")
    parent_name = data.get("parent_name")

    if username and tree_name and parent_name:
        result = json.loads(neo_service.add_parent(username, tree_name, parent_name))
        if result["parent"] is not None:
            return jsonify({"message": "Success: parent added"}), result["status_code"]
        else:
            return jsonify({"message": "Error: parent not added"}), result["status_code"]
    else:
        return jsonify({"message": "Username, tree name, and parent name required"}), 400
    

# Purpose    : adds a child to the in-focus person in the tree
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be modified
#              child (dict)       - dictionary matching the Person class
#              definition
# Returns    : a tuple containing a json string with a message saying whether
#              or not the child was added successfully, as well as an HTTP
#              status code
#              ({"message" : "Success: child added"}, 200)
@app.route('/api/add_child', methods = ["POST"])
def add_parent():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")
    child_name = data.get("child_name")

    if username and tree_name and child_name:
        result = json.loads(neo_service.add_parent(username, tree_name, child_name))
        if result["child"] is not None:
            return jsonify({"message": "Success: child added"}), result["status_code"]
        else:
            return jsonify({"message": "Error: child not added"}), result["status_code"]
    else:
        return jsonify({"message": "Username, tree name, and child name required"}), 400

# Purpose    : adds a spouse to the in-focus person in the tree
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be modified
#              spouse (dict)      - dictionary matching the Person class
#              definition
# Returns    : a tuple containing a json string with a message saying whether
#              or not the spouse was added successfully, as well as an HTTP
#              status code
#              ({"message" : "Success: spouse added"}, 200)
@app.route('/api/add_spouse', methods = ["POST"])
def add_parent():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")
    spouse_name = data.get("spouse")

    if username and tree_name and spouse_name:
        result = json.loads(neo_service.add_parent(username, tree_name, spouse_name))
        if result["spouse"] is not None:
            return jsonify({"message": "Success: spouse added"}), result["status_code"]
        else:
            return jsonify({"message": "Error: spouse not added"}), result["status_code"]
    else:
        return jsonify({"message": "Username, tree name, and spouse name required"}), 400

# Purpose    : divorces the in-focus person from their current spouse
# Parameters : none (retrieves from a posted json, which should have:
#              username (string)  - username of user whose tree it is
#              tree_name (string) - name of tree to be modified
# Returns    : a tuple containing a json string with a message saying whether
#              or not the spouse was divorced successfully, as well as an HTTP
#              status code
#              ({"message" : "Success: spouse divorced"}, 200)
@app.route('/api/divorce', methods = ["POST"])
def add_parent():
    data = request.get_json()
    username = data.get("username")
    tree_name = data.get("tree_name")

    if username and tree_name:
        result = json.loads(neo_service.add_parent(username, tree_name))
        if result["ex_spouse"] is not None:
            return jsonify({"message": "Success: spouse divorced"}), result["status_code"]
        else:
            return jsonify({"message": "Error: spouse not divorced"}), result["status_code"]
    else:
        return jsonify({"message": "Username and tree name required"}), 400


