import pytest
import models

@pytest.fixture(autouse=True)
def run_around_tests(test_db):
    # Insert mock data
    employees = [
        models.Employee(full_name="A", job_title="Dev", country="India", salary=100000),
        models.Employee(full_name="B", job_title="Dev", country="India", salary=200000),
        models.Employee(full_name="C", job_title="Manager", country="India", salary=300000),
        models.Employee(full_name="D", job_title="Dev", country="US", salary=150000),
        models.Employee(full_name="E", job_title="Manager", country="US", salary=250000),
    ]
    test_db.add_all(employees)
    test_db.commit()

def test_country_metrics(client):
    response = client.get("/metrics/country/India")
    assert response.status_code == 200
    data = response.json()
    assert data["country"] == "India"
    assert data["min_salary"] == 100000
    assert data["max_salary"] == 300000
    assert data["avg_salary"] == 200000 # (100k + 200k + 300k) / 3

def test_country_metrics_not_found(client, test_db):
    response = client.get("/metrics/country/Mars")
    assert response.status_code == 404

def test_job_title_metrics(client):
    response = client.get("/metrics/job_title/Dev")
    assert response.status_code == 200
    data = response.json()
    assert data["job_title"] == "Dev"
    assert data["avg_salary"] == 150000 # (100k + 200k + 150k) / 3
