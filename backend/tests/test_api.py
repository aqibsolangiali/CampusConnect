import os
os.environ["DATABASE_URL"] = "sqlite:///./campusconnect_test.db"
from fastapi.testclient import TestClient
from app.main import app


def test_health_and_course_catalog():
    with TestClient(app) as client:
        assert client.get("/api/health").json() == {"status": "ok"}
        response = client.get("/api/courses")
        assert response.status_code == 200
        assert len(response.json()) > 0


def test_register_enroll_and_bookmark():
    import uuid
    with TestClient(app) as client:
        email = f"test-{uuid.uuid4().hex}@example.com"
        r = client.post("/api/auth/register", json={"name": "Test Student", "email": email, "password": "long-password-123"})
        assert r.status_code == 201, r.text
        headers = {"Authorization": "Bearer " + r.json()["access_token"]}
        assert client.get("/api/users/me", headers=headers).json()["email"] == email
        assert client.get("/api/enrollments").status_code == 401
        course = client.get("/api/courses").json()[0]
        assert client.post(f"/api/enrollments/{course['id']}", headers=headers).status_code == 201
        assert client.post(f"/api/enrollments/{course['id']}", headers=headers).status_code == 409
        assert course["id"] in client.get("/api/enrollments", headers=headers).json()
        op = client.get("/api/opportunities").json()[0]
        assert client.post(f"/api/bookmarks/{op['id']}", headers=headers).status_code == 201
        assert op["id"] in client.get("/api/bookmarks", headers=headers).json()
        assert client.delete(f"/api/bookmarks/{op['id']}", headers=headers).status_code == 200
        assert client.delete(f"/api/enrollments/{course['id']}", headers=headers).status_code == 200
