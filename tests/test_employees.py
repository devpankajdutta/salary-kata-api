def test_create_employee(client):
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

def test_read_employee(client):
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

def test_read_employee_not_found(client):
    response = client.get("/employees/999")
    assert response.status_code == 404

def test_read_employees(client):
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

def test_update_employee(client):
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

def test_delete_employee(client):
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

