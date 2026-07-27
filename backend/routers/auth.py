import pandas as pd
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

MEMBERS_CSV = "data/members.csv"


# 프론트에서 로그인 요청 보낼 때 body로 들어오는 값의 형태를 정의
# FastAPI가 이 형태에 안 맞으면 자동으로 에러를 내줌 (직접 검증 코드 안 짜도 됨)
class LoginRequest(BaseModel):
    company_name: str
    employee_id: str
    employee_name: str


# 로그인 화면의 "Company Name" 드롭다운을 채우기 위한 회사 목록 API
@router.get("/companies")
def list_companies():
    df = pd.read_csv(MEMBERS_CSV)
    return {"companies": sorted(df["company_name"].unique().tolist())}


# 회사명 + 사번 + 이름 3개가 CSV의 한 행과 정확히 일치하면 로그인 성공으로 처리
# (원래 Streamlit 버전의 handle_login 로직을 그대로 옮긴 것)
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
