import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

SQLALCHEMY_DATABASE_URL = "sqlite:///./test_metrics.db"
test_engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

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
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    
    # Insert mock data
    employees = [
        models.Employee(full_name="A", job_title="Dev", country="India", salary=100000),
        models.Employee(full_name="B", job_title="Dev", country="India", salary=200000),
        models.Employee(full_name="C", job_title="Manager", country="India", salary=300000),
        models.Employee(full_name="D", job_title="Dev", country="US", salary=150000),
        models.Employee(full_name="E", job_title="Manager", country="US", salary=250000),
    ]
    db.add_all(employees)
    db.commit()
    db.close()
    
    yield
    Base.metadata.drop_all(bind=test_engine)

def test_country_metrics():
    response = client.get("/metrics/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "India"
    assert data["min_salary"] == 100000
    assert data["max_salary"] == 300000
    assert data["avg_salary"] == 200000 # (100k + 200k + 300k) / 3

def test_country_metrics_not_found():
    response = client.get("/metrics/country/Mars")
    assert response.status_code == 404

def test_job_title_metrics():
    response = client.get("/metrics/job_title/Dev")
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Dev"
    assert data["avg_salary"] == 150000 # (100k + 200k + 150k) / 3
