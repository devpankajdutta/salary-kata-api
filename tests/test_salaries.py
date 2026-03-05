import models

def create_mock_employee(db, country: str, salary: float):
    db_emp = models.Employee(
        full_name="Mock Emp",
        job_title="Dev",
        country=country,
        salary=salary
    )
    db.add(db_emp)
    db.commit()
    db.refresh(db_emp)
    return db_emp.id

def test_salary_calculation_india(client, test_db):
    # India: 10% deduction
    emp_id = create_mock_employee(test_db, "India", 100000)
    response = client.get(f"/salaries/{emp_id}/calculate")
    assert response.status_code == 200
    data = response.json()
    assert data["gross_salary"] == 100000
    assert data["deduction_percentage"] == 10.0
    assert data["deduction_amount"] == 10000
    assert data["net_salary"] == 90000

def test_salary_calculation_us(client, test_db):
    # US: 12% deduction
    emp_id = create_mock_employee(test_db, "United States", 100000)
    response = client.get(f"/salaries/{emp_id}/calculate")
    assert response.status_code == 200
    data = response.json()
    assert data["deduction_percentage"] == 12.0
    assert data["net_salary"] == 88000

def test_salary_calculation_other(client, test_db):
    # Other: 0% deduction
    emp_id = create_mock_employee(test_db, "UK", 100000)
    response = client.get(f"/salaries/{emp_id}/calculate")
    assert response.status_code == 200
    data = response.json()
    assert data["deduction_percentage"] == 0.0
    assert data["net_salary"] == 100000

def test_salary_calculation_not_found(client, test_db):
    response = client.get("/salaries/999/calculate")
    assert response.status_code == 404
