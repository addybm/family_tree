from flask import Flask, jsonify, request
from flask_cors import CORS
import atexit
from neo4j_service import Neo4jService
import json


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
    return jsonify({'users' : users, 'trees' : trees})

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
    # data = request.get_json()
    # username = data.get("username")
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
