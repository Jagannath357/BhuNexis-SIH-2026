import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "project" in data
    assert data["project"] == "BhuNexis API"

def test_health_endpoint():
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "HEALTHY"
    assert "backend" in data["services"]
    assert "database" in data["services"]
    assert data["services"]["ocr"]["status"] == "UNAVAILABLE"

def test_admin_login_success():
    payload = {
        "email": "admin@bhunexis.demo",
        "password": "password123",
        "role": "ADMIN"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["user"]["role"] == "ADMIN"

def test_login_role_mismatch():
    payload = {
        "email": "admin@bhunexis.demo",
        "password": "password123",
        "role": "OFFICER"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 403
    data = response.json()
    assert data["error"]["code"] == "ROLE_MISMATCH"

def test_citizen_login_success():
    payload = {
        "email": "citizen@bhunexis.demo",
        "password": "password123",
        "role": "CITIZEN"
    }
    response = client.post("/api/v1/auth/login", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["user"]["role"] == "CITIZEN"
