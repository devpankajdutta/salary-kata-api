from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/metrics",
    tags=["metrics"]
)

@router.get("/country/{country}", response_model=schemas.CountryMetricsResponse)
def get_country_metrics(country: str, db: Session = Depends(get_db)):
    # Standardize country search (case-insensitive for simplicity, though exact match is used here)
    metrics = db.query(
        func.min(models.Employee.salary).label("min_salary"),
        func.max(models.Employee.salary).label("max_salary"),
        func.avg(models.Employee.salary).label("avg_salary")
    ).filter(models.Employee.country.ilike(country)).first()

    if metrics.min_salary is None:
        raise HTTPException(status_code=404, detail="No employees found for this country")

    return schemas.CountryMetricsResponse(
        country=country,
        min_salary=metrics.min_salary,
        max_salary=metrics.max_salary,
        avg_salary=metrics.avg_salary
    )

@router.get("/job_title/{job_title}", response_model=schemas.JobTitleMetricsResponse)
def get_job_title_metrics(job_title: str, db: Session = Depends(get_db)):
    metrics = db.query(
        func.avg(models.Employee.salary).label("avg_salary")
    ).filter(models.Employee.job_title.ilike(job_title)).first()

    if metrics.avg_salary is None:
        raise HTTPException(status_code=404, detail="No employees found for this job title")

    return schemas.JobTitleMetricsResponse(
        job_title=job_title,
        avg_salary=metrics.avg_salary
    )
