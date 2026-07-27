from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, scanner, chatbot, menu, test

app = FastAPI(title="AI Study Backend")

# React(5173/5174)에서 오는 요청만 허용 - 프론트와 백엔드가 다른 포트라 CORS 설정이 필요함
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 기능별로 라우터 파일을 나눠서 등록 (prefix가 실제 API 경로 앞부분이 됨)
# 예: auth.router 안의 "/login" -> 실제 경로는 "/api/auth/login"
app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(scanner.router, prefix="/api/scanner", tags=["scanner"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(menu.router, prefix="/api/menu", tags=["menu"])
app.include_router(test.router, prefix="/api/test", tags=["test"])


# 서버가 살아있는지 확인용 (프론트에서 굳이 안 써도 되고, 브라우저로 직접 들어가 확인 가능)
@app.get("/api/health")
def health():
    return {"status": "ok"}
