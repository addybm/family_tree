from flask import Flask, jsonify, request
from flask_cors import CORS
import atexit
from neo4j_service import Neo4jService
# from neo4j_service import get_users

app = Flask(__name__)
CORS(app)  # Allow cross-origin requests (for React)
neo_service = Neo4jService()

# driver = GraphDatabase.driver(NEO4J_URI, auth = (NEO4J_USERNAME, NEO4J_PASSWORD))

# @app.route('/test_db', methods = ['GET'])
# def test_db():
#     with driver.session() as session:
#         result = session.run("RETURN 'Connected to Neo4j' AS message")
#         return jsonify({"message" : result.single()["message"]})
    
# @app.route('/people', methods = ['GET'])
# def get_people():
#     with driver.session() as session:
#         result = session.run("MATCH (p:Person) RETURN p.name AS name")
#         people = [record["name"] for record in result]
#         return jsonify({"people": people})

# @app.route('/data', methods=['GET'])
# def hello():
#     return jsonify({"message": "Hello from Python!"})





@app.route('/people', methods=['GET'])
def people():
    # return jsonify({"people": get_people()})
    users = neo_service.get_users()
    return jsonify({'users' : users})


@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if username and password:
        result = neo_service.create_user(username, password)
        return jsonify({"message": "User registered successfully", "user": result}), 201
    else:
        return jsonify({"message": "Username and password required"}), 400

# @app.route('/api/login', methods=['POST'])
# def login():
#     data = request.get_json()
#     username = data.get("username")
#     password = data.get("password")
    
#     if username and password:
#         is_valid = neo_service.validate_user(username, password)
#         if is_valid:
#             return jsonify({"message": "Login successful"}), 200
#         else:
#             return jsonify({"message": "Invalid username or password"}), 401
#     else:
#         return jsonify({"message": "Username and password required"}), 400

if __name__ == '__main__':
    app.run(debug = True, port = 5002)