import pytest
from fastapi.testclient import TestClient
from main import app
from database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import models

# Reuse test db logic
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_salaries.db"
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
    yield
    Base.metadata.drop_all(bind=test_engine)

def create_mock_employee(country: str, salary: float):
    db_emp = models.Employee(
        full_name="Mock Emp",
        job_title="Dev",
        country=country,
        salary=salary
    )
    db = TestingSessionLocal()
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    db.close()
    return db_emp.id

def test_salary_calculation_india():
    # India: 10% deduction
    emp_id = create_mock_employee("India", 100000)
    response = client.get(f"/salaries/{emp_id}/calculate")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000
    assert data["deduction_percentage"] == 10.0
    assert data["deduction_amount"] == 10000
    assert data["net_salary"] == 90000

def test_salary_calculation_us():
    # US: 12% deduction
    emp_id = create_mock_employee("United States", 100000)
    response = client.get(f"/salaries/{emp_id}/calculate")
    assert response.status_code == 200
    data = response.json()
    assert data["deduction_percentage"] == 12.0
    assert data["net_salary"] == 88000

def test_salary_calculation_other():
    # Other: 0% deduction
    emp_id = create_mock_employee("UK", 100000)
    response = client.get(f"/salaries/{emp_id}/calculate")
    assert response.status_code == 200
    data = response.json()
    assert data["deduction_percentage"] == 0.0
    assert data["net_salary"] == 100000

def test_salary_calculation_not_found():
    response = client.get("/salaries/999/calculate")
    assert response.status_code == 404
