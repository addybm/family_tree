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
@app.route('/people', methods = ["GET"])
def people():
    users = neo_service.get_users()
    return jsonify({'users' : users})

# Purpose    : adds a user to the neo4j instance
# Parameters : none (retrieves from a posted json, which should have:)
#              username (string) - username of user to be removed
#              password (string) - password of user to be removed
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
# Parameters : none (retrieves from a posted json, which should have:)
#              username (string) - username of user to be removed
#              password (string) - password of user to be removed
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
# Parameters : none (retrieves from a posted json, which should have:)
#              username (string) - username of user to be removed
#              password (string) - password of user to be removed
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

if __name__ == '__main__':
    app.run(debug = True, port = 5002)
