import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_register_success(client):
    response = client.post('/api/register', json={
        "username": "testuserNEW",
        "password": "testpasswordNEW"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"

# def test_register_missing_fields(client):
#     response = client.post('/api/register', json={"username": "testuser"})
#     assert response.status_code == 400
#     assert "error" in response.get_json()

# def test_login_success(client):
#     # First, register a user
#     client.post('/api/register', json={
#         "username": "testuser",
#         "password": "testpassword"
#     })
    
#     # Then, try to log in
#     response = client.post('/api/login', json={
#         "username": "testuser",
#         "password": "testpassword"
#     })
#     assert response.status_code == 200
#     assert response.get_json()["message"] == "Login successful"

# def test_login_invalid_password(client):
#     client.post('/api/register', json={
#         "username": "testuser",
#         "password": "testpassword"
#     })
    
#     response = client.post('/api/login', json={
#         "username": "testuser",
#         "password": "wrongpassword"
#     })
#     assert response.status_code == 401
#     assert response.get_json()["error"] == "Invalid credentials"

# def test_login_nonexistent_user(client):
#     response = client.post('/api/login', json={
#         "username": "nonexistent",
#         "password": "password"
#     })
#     assert response.status_code == 404
#     assert response.get_json()["error"] == "User not found"
