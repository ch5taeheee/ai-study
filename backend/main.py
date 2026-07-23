from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers import auth, scanner, chatbot, menu

app = FastAPI(title="AI Study Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
app.include_router(scanner.router, prefix="/api/scanner", tags=["scanner"])
app.include_router(chatbot.router, prefix="/api/chatbot", tags=["chatbot"])
app.include_router(menu.router, prefix="/api/menu", tags=["menu"])


@app.get("/api/health")
def health():
    return {"status": "ok"}
