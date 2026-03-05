# Salary Kata API

A simple API to calculate and provide metrics for employee salaries. This project was developed strictly adhering to Test-Driven Development (TDD) and the given constraints (using SQLite).

## Technology Stack
- **Python 3**
- **FastAPI**: Chosen for its high performance, automatic data validation, and built-in interactive documentation (Swagger UI).
- **SQLAlchemy (SQLite)**: Used as the ORM to interact with the requested Sqlite database smoothly.
- **Pytest**: Chosen to run the TDD iterations and verify the correctness of the API endpoints.

## Implementation Details

### TDD Process
The commit history strictly reflects the Test-Driven Development (TDD) loop. Branches/commits were made following the sequence:
1. Write failing tests for an endpoint behavior (Red).
2. Implement the minimal necessary FastAPI routing, Pydantic schema, and SQLAlchemy logic (Green).
3. Refactor and ensure all tests pass.

### Endpoints
- **Employee CRUD**: `/employees/` supports creating, reading, updating, and deleting employees.
- **Salary Calculation**: `/salaries/{employee_id}/calculate` handles country-specific salary deductions (India: 10%, US: 12%, Others: 0%).
- **Salary Metrics**: `/metrics/country/{country}` (Provides min, max, avg) and `/metrics/job_title/{job_title}` (Provides avg).

### AI Usage Disclosure
I utilized AI as an autonomous coding assistant (`Antigravity/Agentic Coding`) to implement this API.
- **Tools Used**: Google DeepMind Antigravity framework.
- **Process/Rationale**: I acted as an orchestrator, requesting the AI to break down the exercise into an actionable TDD checklist. Then, I requested the AI to execute the tasks sequentially. It scaffolded the tests, generated the implementation files, and committed the changes automatically upon passing tests. This showcases a modern way to delegate rote implementation tasks to an LLM agent, accelerating delivery time to production while upholding software quality standards (enforcing test coverage and modularity).

## How to Run the Project

1. Keep using your virtual environment (or create one):
```bash
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Unix/Mac:
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the tests:
```bash
pytest
```

4. Run the API Server:
```bash
uvicorn main:app --reload
```
You can access the auto-generated API documentation by navigating to `http://127.0.0.1:8000/docs`.
