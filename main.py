from fastapi import FastAPI
from database import engine, Base
from routers import employees, salaries, metrics

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Salary Kata API")

app.include_router(employees.router)
app.include_router(salaries.router)
app.include_router(metrics.router)
