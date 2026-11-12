
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response

from pydantic import BaseModel
from agent import get_hr_response

app = FastAPI(
    title="HR Policy Assistant API"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    message: str


@app.get("/")
def home():
    return {
        "message": "HR Policy Assistant API is running"
    }


# Favicon route - returns 200 OK
@app.get("/favicon.ico", include_in_schema=False)
def favicon():
    return Response(
        content=b"",
        media_type="image/x-icon",
        status_code=200
    )


@app.post("/api/chat")
def chat(request: ChatRequest):

    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Please enter a question"
        )

    try:
        answer = get_hr_response(request.message)

        return {
            "answer": answer
        }

    except Exception as error:
        print("Chat error:", error)

        raise HTTPException(
            status_code=500,
            detail="Unable to process your question"
        )
