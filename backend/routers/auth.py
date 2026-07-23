import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

MEMBERS_CSV = "data/members.csv"


class LoginRequest(BaseModel):
    company_name: str
    employee_id: str
    employee_name: str


@router.get("/companies")
def list_companies():
    df = pd.read_csv(MEMBERS_CSV)
    return {"companies": sorted(df["company_name"].unique().tolist())}


@router.post("/login")
def login(payload: LoginRequest):
    df = pd.read_csv(MEMBERS_CSV)
    matched = df[
        (df["company_name"] == payload.company_name)
        & (df["employee_id"].astype(str) == payload.employee_id.strip())
        & (df["employee_name"] == payload.employee_name.strip())
    ]

    if matched.empty:
        raise HTTPException(status_code=401, detail="일치하는 정보가 없습니다.")

    return matched.iloc[0].to_dict()
