import pytest
from server import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client

# Login/account tests
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

# Tree array tests

# test getting trees
def test_get_trees_nonexistent_user(client):
    response = client.get('/api/trees?username=doesnotexist')
    assert response.status_code == 404
    assert response.get_json()["tree_names"] is None

def test_get_trees_username_not_provided(client):
    response = client.get('/api/trees', json = {})
    assert response.status_code == 400
    assert response.get_json()["tree_names"] is None

def test_user_no_trees(client):
    # add a user
    client.post('/api/register', json = {
        "username" : "testusernotrees",
        "password" : "testpassword"
    })

    response = client.get('/api/trees?username=testusernotrees')

    assert response.status_code == 200
    assert response.get_json()["tree_names"] == []

    # remove user
    client.post('/api/remove', json = {
        "username" : "testusernotrees",
        "password" : "testpassword"
    })

# test adding a tree

# add a user and a tree, then try retrieving the trees, removing the tree, and removing the user
def test_add_tree(client):
    # add a user
    test_register_user(client)

    response = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })
    
    assert response.status_code == 201
    assert response.get_json()["message"] == "Success: tree: tree1 created"

    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert response_get.get_json()["tree_names"] == ["tree1"]

    test_remove_user(client)

def test_add_multiple_trees(client):
    # add a user
    test_register_user(client)

    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })
    
    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree1 created"

    response_second = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree2"
    })
    
    assert response_second.status_code == 201
    assert response_second.get_json()["message"] == "Success: tree: tree2 created"

    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert sorted(response_get.get_json()["tree_names"]) == sorted(["tree1", "tree2"])

    test_remove_user(client)

def test_add_tree_no_username(client):
    response = client.post('/api/add_tree', json = {
        "tree_name" : "tree1"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and tree name required"

def test_add_tree_no_tree_name(client):
    response = client.post('/api/add_tree', json = {
        "username" : "testuser"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and tree name required"

def test_add_tree_no_username_or_tree_name(client):
    response = client.post('/api/add_tree', json = {})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and tree name required"

def test_add_tree_nonexistent_user(client):
    response = client.post('/api/add_tree', json = {
        "username" : "doesnotexist",
        "tree_name" : "tree1"
    })
    assert response.status_code == 500
    assert response.get_json()["message"] == "Error: tree not created"

def test_add_tree_duplicate_tree(client):
    # add a user
    test_register_user(client)

    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree1 created"

    response_second = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_second.status_code == 409
    assert response_second.get_json()["message"] == "Error: tree not created"

    test_remove_user(client)

# test removing a tree

def test_remove_tree(client):
    # add a user
    test_register_user(client)

    # add a tree
    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree1 created"

    # remove the tree
    response_second = client.post('/api/remove_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_second.status_code == 200
    assert response_second.get_json()["message"] == "Success: 1 tree(s) removed"

    # get the trees
    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert response_get.get_json()["tree_names"] == []

    test_remove_user(client)

def test_remove_trees(client):
    # add a user
    test_register_user(client)

    # add a tree
    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree1 created"

    # add a tree
    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree2"
    })

    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree2 created"

    # remove a tree
    response_second = client.post('/api/remove_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_second.status_code == 200
    assert response_second.get_json()["message"] == "Success: 1 tree(s) removed"

    # get the trees
    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert response_get.get_json()["tree_names"] == ["tree2"]

    test_remove_user(client)

def test_remove_tree_no_username(client):
    response = client.post('/api/remove_tree', json = {
        "tree_name" : "tree1"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and tree name required"

def test_remove_tree_no_tree_name(client):
    response = client.post('/api/remove_tree', json = {
        "username" : "testuser"
    })
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and tree name required"

def test_remove_tree_no_username_or_tree_name(client):
    response = client.post('/api/remove_tree', json = {})
    assert response.status_code == 400
    assert response.get_json()["message"] == "Username and tree name required"

def test_remove_tree_nonexistent_user(client):
    response = client.post('/api/remove_tree', json = {
        "username" : "doesnotexist",
        "tree_name" : "tree1"
    })
    assert response.status_code == 500
    assert response.get_json()["message"] == "Error: tree not removed"

def test_remove_tree_nonexistent_tree(client):
    # add a user
    test_register_user(client)

    response = client.post('/api/remove_tree', json =
    {
        "username" : "testuser",
        "tree_name" : "doesnotexist"
    })

    assert response.status_code == 500
    assert response.get_json()["message"] == "Error: tree not removed"

    test_remove_user(client)

# test modifying last_opened

def test_modify_last_opened(client):
    # add a user
    test_register_user(client)

    # add a tree
    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree1 created"

     # add a tree
    response_first = client.post('/api/add_tree', json = {
        "username" : "testuser",
        "tree_name" : "tree2"
    })

    assert response_first.status_code == 201
    assert response_first.get_json()["message"] == "Success: tree: tree2 created"

    # get the trees
    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert sorted(response_get.get_json()["tree_names"]) == sorted(["tree1","tree2"])

    # modify last_opened
    response_second = client.post('/api/modify_last_opened', json = {
        "username" : "testuser",
        "tree_name" : "tree1"
    })

    assert response_second.status_code == 200

    # get the trees
    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert response_get.get_json()["tree_names"] == ["tree1","tree2"]

    # modify last_opened
    response_second = client.post('/api/modify_last_opened', json = {
        "username" : "testuser",
        "tree_name" : "tree2"
    })

    assert response_second.status_code == 200

    # get the trees
    response_get = client.get('/api/trees?username=testuser')

    assert response_get.status_code == 200
    assert response_get.get_json()["tree_names"] == ["tree2","tree1"]

    test_remove_user(client)

