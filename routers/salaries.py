from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import models, schemas

router = APIRouter(
    prefix="/salaries",
    tags=["salaries"]
)

@router.get("/{employee_id}/calculate", response_model=schemas.SalaryCalculationResponse)
def calculate_salary(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(models.Employee.id == employee_id).first()
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    gross = employee.salary
    country = employee.country.lower()

    if country == "india":
        deduction_pct = 10.0
    elif country == "united states":
        deduction_pct = 12.0
    else:
        deduction_pct = 0.0

    deduction_amount = (gross * deduction_pct) / 100.0
    net_salary = gross - deduction_amount

    return schemas.SalaryCalculationResponse(
        employee_id=employee_id,
        gross_salary=gross,
        deduction_percentage=deduction_pct,
        deduction_amount=deduction_amount,
        net_salary=net_salary
    )
