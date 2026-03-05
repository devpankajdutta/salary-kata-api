from pydantic import BaseModel

class EmployeeBase(BaseModel):
    full_name: str
    job_title: str
    country: str
    salary: float

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeResponse(EmployeeBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class SalaryCalculationResponse(BaseModel):
    employee_id: int
    gross_salary: float
    deduction_percentage: float
    deduction_amount: float
    net_salary: float

class CountryMetricsResponse(BaseModel):
    country: str
    min_salary: float
    max_salary: float
    avg_salary: float

class JobTitleMetricsResponse(BaseModel):
    job_title: str
    avg_salary: float
