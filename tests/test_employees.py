import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: create tables
    Base.metadata.create_all(bind=test_engine)
    yield
    # Teardown: drop tables
    Base.metadata.drop_all(bind=test_engine)

def test_create_employee():
    response = client.post(
        "/employees/",
        json={
            "full_name": "John Doe",
            "job_title": "Software Engineer",
            "country": "United States",
            "salary": 100000
        },
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["full_name"] == "John Doe"
    assert data["job_title"] == "Software Engineer"
    assert data["country"] == "United States"
    assert "id" in data

def test_read_employee():
    # First create
    create_response = client.post(
        "/employees/",
        json={
            "full_name": "Jane Smith",
            "job_title": "Product Manager",
            "country": "India",
            "salary": 1500000
        },
    )
    assert create_response.status_code == 201
    emp_id = create_response.json()["id"]

    # Then read
    read_response = client.get(f"/employees/{emp_id}")
    assert read_response.status_code == 200
    read_data = read_response.json()
    assert read_data["full_name"] == "Jane Smith"
    assert read_data["id"] == emp_id

def test_read_employee_not_found():
    response = client.get("/employees/999")
    assert response.status_code == 404

def test_read_employees():
    client.post(
        "/employees/",
        json={"full_name": "A", "job_title": "B", "country": "C", "salary": 10}
    )
    client.post(
        "/employees/",
        json={"full_name": "D", "job_title": "E", "country": "F", "salary": 20}
    )
    response = client.get("/employees/")
    assert response.status_code == 200
    assert len(response.json()) >= 2

def test_update_employee():
    # Create
    create_resp = client.post(
        "/employees/",
        json={"full_name": "Updatable", "job_title": "Old Title", "country": "US", "salary": 50}
    )
    emp_id = create_resp.json()["id"]

    # Update
    update_resp = client.put(
        f"/employees/{emp_id}",
        json={"full_name": "Updated", "job_title": "New Title", "country": "UK", "salary": 60}
    )
    assert update_resp.status_code == 200
    updated_data = update_resp.json()
    assert updated_data["job_title"] == "New Title"

    # Verify update
    read_resp = client.get(f"/employees/{emp_id}")
    assert read_resp.json()["job_title"] == "New Title"

def test_delete_employee():
    # Create
    create_resp = client.post(
        "/employees/",
        json={"full_name": "Deletable", "job_title": "Delete Title", "country": "CA", "salary": 70}
    )
    emp_id = create_resp.json()["id"]

    # Delete
    delete_resp = client.delete(f"/employees/{emp_id}")
    assert delete_resp.status_code == 204

    # Verify deletion
    read_resp = client.get(f"/employees/{emp_id}")
    assert read_resp.status_code == 404

