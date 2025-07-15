import pytest
import tempfile
import os
from app import app, init_db


@pytest.fixture
def client():
    # Create a temporary database
    db_fd, app.config["DATABASE"] = tempfile.mkstemp()
    app.config["TESTING"] = True

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(app.config["DATABASE"])


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
