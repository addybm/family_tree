import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

def test_register_user(client):
    response = client.post('/api/register', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response.status_code == 201
    assert response.get_json()["message"] == "User registered successfully"
    assert response.get_json()["user"] == "testuser"

def test_login_valid(client):
    response = client.post('/api/login', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "User credentials valid"

def test_login_invalid_password(client):
    response = client.post('/api/login', json = {
        "username" : "testuser",
        "password" : "wrongpassword"
    })
    assert response.status_code == 401
    assert response.get_json()["message"] == "User credentials invalid"

def test_login_non_existent_user(client):
    response = client.post('/api/login', json = {
        "username" : "testuserdoesnotexist",
        "password" : "password"
    })
    assert response.status_code == 404
    assert response.get_json()["message"] == "User credentials invalid"

def test_login_no_password(client):
    response = client.post('/api/login', json = {
        "username" : "testuser",
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Existing username and password required"

def test_login_no_username(client):
    response = client.post('/api/login', json = {
        "password" : "testuser",
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Existing username and password required"

def test_remove_user(client):
    response = client.post('/api/remove', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response.status_code == 200
    assert response.get_json()["message"] == "User removed successfully"

# try adding the same user twice, then remove the user
def test_register_duplicate(client):
    response_first = client.post('/api/register', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "User registered successfully"
    assert response_first.get_json()["user"] == "testuser"

    response_second = client.post('/api/register', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response_second.status_code == 409
    assert response_second.get_json()["message"] == "User not registered successfully"
    assert response_second.get_json()["user"] == "testuser"

    response_third = client.post('/api/remove', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response_third.status_code == 200
    assert response_third.get_json()["message"] == "User removed successfully"

def test_remove_wrong_password(client):
    response_first = client.post('/api/register', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "User registered successfully"
    assert response_first.get_json()["user"] == "testuser"

    response_second = client.post('/api/remove', json = {
        "username" : "testuser",
        "password" : "testpasswordWRONG"
    })
    assert response_second.status_code == 401
    assert response_second.get_json()["message"] == "User not removed"

    response_third = client.post('/api/remove', json = {
        "username" : "testuser",
        "password" : "testpassword"
    })
    assert response_third.status_code == 200
    assert response_third.get_json()["message"] == "User removed successfully"

def test_password_too_short(client):
    response = client.post('/api/register', json = {
        "username" : "testuser",
        "password" : "short"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "User not registered successfully"
    assert response.get_json()["user"] == "testuser"

def test_register_missing_password(client):
    response = client.post('/api/register', json = {"username" : "testuser"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password required"
    assert response.get_json()["user"] == "testuser"

def test_register_missing_username(client):
    response = client.post('/api/register', json = {"password" : "testuser"})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and password required"
    assert response.get_json()["user"] == None


def test_remove_non_existent_user(client):
    response = client.post('/api/remove', json = {
        "username" : "doesnotexist",
        "password" : "doesnotmatter"
    })
    assert response.status_code == 404
    assert response.get_json(["message"] == "User not removed")

