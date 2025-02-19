import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_register_user(client):
    response = client.post('/api/register', json = {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"

def test_remove_user(client):
    response = client.post('/api/remove', json = {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "User removed successfully"

# try adding the same user twice, then remove the user
def test_register_duplicate(client):
    response_first = client.post('/api/register', json = {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "User registered successfully"
    response_second = client.post('/api/register', json = {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response_second.status_code == 409
    assert response_second.get_json()["message"] == "User not registered successfully"
    response_third = client.post('/api/remove', json = {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response_third.status_code == 200
    assert response_third.get_json()["message"] == "User removed successfully"

def test_remove_wrong_password(client):
    response_first = client.post('/api/register', json = {
    "username": "testuser",
    "password": "testpassword"
    })
    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "User registered successfully"
    response_second = client.post('/api/remove', json = {
        "username": "testuser",
        "password": "testpasswordWRONG"
    })
    assert response_second.status_code == 404
    assert response_second.get_json()["message"] == "User not removed"
    response_third = client.post('/api/remove', json = {
        "username": "testuser",
        "password": "testpassword"
    })
    assert response_third.status_code == 200
    assert response_third.get_json()["message"] == "User removed successfully"


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
