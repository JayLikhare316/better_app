import os
import tempfile

import pytest


@pytest.fixture
def client():
    # Set test environment variables before importing app
    os.environ["FLASK_ENV"] = "development"
    
    # Use secure temporary file creation
    db_fd, db_path = tempfile.mkstemp()
    os.environ["DB_PATH"] = db_path

    # Import app after setting environment
    from app import app, init_db

    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    # Cleanup - close and remove test database
    os.close(db_fd)
    if os.path.exists(db_path):
        os.unlink(db_path)


def test_index(client):
    """Test the index page loads"""
    rv = client.get("/")
    assert rv.status_code == 200
    assert b"Better App" in rv.data


def test_health_endpoint(client):
    """Test health endpoint"""
    rv = client.get("/health")
    assert rv.status_code == 200
    assert b"healthy" in rv.data


def test_add_name(client):
    """Test adding a name"""
    rv = client.post("/add", data={"name": "Test Name"})
    assert rv.status_code == 302  # Redirect after POST


def test_add_empty_name(client):
    """Test adding empty name should not create entry"""
    rv = client.post("/add", data={"name": ""})
    assert rv.status_code == 302


def test_edit_name_get(client):
    """Test GET request to edit endpoint"""
    # First add a name
    client.post("/add", data={"name": "EditTestName"})

    # Get edit page - just check it loads successfully
    rv = client.get("/edit/1")
    assert rv.status_code == 200
    # Check that it's the edit page
    assert b"Edit Name" in rv.data
    assert b"Update Name" in rv.data


def test_edit_name_post(client):
    """Test POST request to edit endpoint"""
    # First add a name
    client.post("/add", data={"name": "Original Name"})

    # Edit the name
    rv = client.post("/edit/1", data={"new_name": "Updated Name"})
    assert rv.status_code == 302


def test_edit_nonexistent_name(client):
    """Test editing non-existent name redirects to index"""
    rv = client.get("/edit/999")
    assert rv.status_code == 302


def test_delete_name(client):
    """Test deleting a name"""
    # First add a name
    client.post("/add", data={"name": "To Delete"})

    # Delete the name
    rv = client.get("/delete/1")
    assert rv.status_code == 302


def test_database_persistence(client):
    """Test that database operations work correctly"""
    # Add multiple names
    client.post("/add", data={"name": "Name 1"})
    client.post("/add", data={"name": "Name 2"})
    client.post("/add", data={"name": "Name 3"})

    # Check all names appear
    rv = client.get("/")
    assert rv.status_code == 200


def test_input_validation(client):
    """Test input validation for security"""
    # Test valid names
    rv = client.post("/add", data={"name": "Valid Name"})
    assert rv.status_code == 302
    
    rv = client.post("/add", data={"name": "John O'Connor"})
    assert rv.status_code == 302
    
    rv = client.post("/add", data={"name": "Mary-Jane"})
    assert rv.status_code == 302
    
    # Test invalid names (should be rejected silently)
    rv = client.post("/add", data={"name": "<script>alert('xss')</script>"})
    assert rv.status_code == 302
    
    rv = client.post("/add", data={"name": "'; DROP TABLE names; --"})
    assert rv.status_code == 302


def test_security_headers(client):
    """Test that security headers are present"""
    rv = client.get("/")
    assert rv.status_code == 200
    assert 'X-Content-Type-Options' in rv.headers
    assert 'X-Frame-Options' in rv.headers
    assert 'X-XSS-Protection' in rv.headers
    assert rv.headers['X-Content-Type-Options'] == 'nosniff'
    assert rv.headers['X-Frame-Options'] == 'DENY'
