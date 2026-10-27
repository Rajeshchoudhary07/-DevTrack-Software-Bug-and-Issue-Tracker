import pytest
from app import create_app, db

@pytest.fixture()
def client(tmp_path):
    database = tmp_path / "test.db"
    app = create_app({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": f"sqlite:///{database}",
    })
    with app.app_context():
        db.drop_all()
        db.create_all()
    with app.test_client() as client:
        yield client
    with app.app_context():
        db.session.remove()
        db.drop_all()

def test_health_endpoint(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "ok"

def test_create_and_get_issue(client):
    response = client.post("/api/issues", json={
        "title": "Login button is broken", "description": "Clicking login does nothing",
        "priority": "High", "assignee": "Asha"
    })
    assert response.status_code == 201
    issue_id = response.get_json()["id"]
    fetched = client.get(f"/api/issues/{issue_id}")
    assert fetched.status_code == 200
    assert fetched.get_json()["title"] == "Login button is broken"

def test_title_is_required(client):
    response = client.post("/api/issues", json={"title": "  "})
    assert response.status_code == 400
    assert "Title is required" in response.get_json()["error"]

def test_update_issue_status(client):
    created = client.post("/api/issues", json={"title": "Broken test"})
    issue_id = created.get_json()["id"]
    response = client.patch(f"/api/issues/{issue_id}", json={"status": "In Progress"})
    assert response.status_code == 200
    assert response.get_json()["status"] == "In Progress"

def test_invalid_status_rejected(client):
    response = client.post("/api/issues", json={"title": "Test", "status": "Blocked"})
    assert response.status_code == 400

def test_filter_issues_by_status(client):
    client.post("/api/issues", json={"title": "Bug A", "status": "Open"})
    client.post("/api/issues", json={"title": "Bug B", "status": "Resolved"})
    response = client.get("/api/issues?status=Resolved")
    assert response.status_code == 200
    assert response.get_json()["count"] == 1
    assert response.get_json()["items"][0]["title"] == "Bug B"

def test_delete_issue(client):
    created = client.post("/api/issues", json={"title": "Delete me"})
    issue_id = created.get_json()["id"]
    assert client.delete(f"/api/issues/{issue_id}").status_code == 200
    assert client.get(f"/api/issues/{issue_id}").status_code == 404
