import asyncio
import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from google import genai
from google.genai import types
from pydantic import BaseModel, Field

load_dotenv()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
API_KEY = os.getenv("GEMINI_API_KEY")


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=20_000)


class ChatResponse(BaseModel):
    reply: str
    model: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not API_KEY:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Create a .env file with GEMINI_API_KEY=your_key"
        )
    app.state.gemini_client = genai.Client(api_key=API_KEY)
    yield


app = FastAPI(
    title="Gemini Flash Chat API",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/health")
def health():
    return {"status": "ok", "model": MODEL_NAME}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest) -> ChatResponse:
    try:
        response = await asyncio.to_thread(
            app.state.gemini_client.models.generate_content,
            model=MODEL_NAME,
            contents=request.message,
        )

        reply = response.text or ""
        if not reply.strip():
            raise RuntimeError("Gemini returned no text.")

        return ChatResponse(reply=reply, model=MODEL_NAME)

    except Exception as exc:
        print(f"\nGemini error type: {type(exc).__name__}")
        print(f"Gemini error detail: {exc}\n")

        raise HTTPException(
            status_code=502,
            detail={
                "message": "Gemini request failed",
                "error_type": type(exc).__name__,
                "upstream_error": str(exc),
            },
        ) from exc


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="127.0.0.1", port=8000, reload=True)
