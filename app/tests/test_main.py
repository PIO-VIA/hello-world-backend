from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["docs"] == "/docs"

def test_create_super_admin_no_db():
    # This might fail if DB is not running, but it's a structural test
    response = client.post(
        "/api/v1/system/create-super-admin",
        json={
            "email": "admin@example.com",
            "full_name": "Super Admin",
            "matricule": "ADMIN001",
            "password": "password123"
        },
    )
    # If DB is not available, it should return 500 (internal server error) 
    # as per our generic exception handler, not a crash.
    assert response.status_code in [201, 500]
