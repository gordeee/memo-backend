from fastapi import FastAPI, Request
from auth import router as auth_router
from memo_ingest import sync_drive_memos
from chat_with_memos import ask_about_memos
from pydantic import BaseModel
from fastapi.responses import RedirectResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

app = FastAPI()
app.include_router(auth_router)
app.add_middleware(SessionMiddleware, secret_key="your-super-secret-session-key")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatQuery(BaseModel):
    question: str

@app.post("/chat-with-memos")
def chat(query: ChatQuery, request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login")
    return ask_about_memos(query.question, user["id"])

@app.post("/sync-memos")
def sync(request: Request):
    user = request.session.get("user")
    if not user:
        return RedirectResponse(url="/login")
    return {"synced_files": sync_drive_memos(user["id"])}

@app.get("/me")
def get_me(request: Request):
    user = request.session.get("user")
    if not user:
        return {"error": "Not authenticated"}
    return user
