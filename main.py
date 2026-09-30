from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from explanation_module import explain_topic
from learning_path import get_learning_recommendations
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie",
    version="1.0.0",
    description="AI-powered learning assistant"
)

app.mount(
    "/static",(BASE_DIR / "static").mkdir(parents=True, exist_ok=True)
    StaticFiles(directory=BASE_DIR / "static"),
    name="static"
)

templates = Jinja2Templates(
    directory=str(BASE_DIR / "templates")
)


# -----------------------------
# Request Models
# -----------------------------

class QARequest(BaseModel):
    question: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )


class ExplainRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=10000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )


class QuizRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )

    count: int = Field(
        default=3,
        ge=1,
        le=10
    )


class SummaryRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=30000
    )


class LearningRequest(BaseModel):
    topic: str = Field(
        ...,
        min_length=1,
        max_length=5000
    )

    level: str = Field(
        default="beginner",
        max_length=50
    )

    weeks: int = Field(
        default=6,
        ge=1,
        le=52
    )


# -----------------------------
# Frontend
# -----------------------------

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )


# -----------------------------
# Health Check
# -----------------------------

@app.get("/health")
async def health():

    return {
        "status": "ok",
        "service": "EduGenie"
    }


# -----------------------------
# Q&A
# -----------------------------

@app.post("/qa")
async def qa(payload: QARequest):

    try:

        answer = answer_question(
            payload.question
        )

        return {
            "answer": answer
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Concept Explanation
# -----------------------------

@app.post("/explain")
async def explain(payload: ExplainRequest):

    try:

        explanation = explain_topic(
            payload.topic,
            payload.level
        )

        return {
            "explanation": explanation
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Quiz
# -----------------------------

@app.post("/quiz")
async def quiz(payload: QuizRequest):

    try:

        quiz = generate_quiz(
            payload.text,
            payload.count
        )

        return {
            "quiz": quiz
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Summarization
# -----------------------------

@app.post("/summarize")
async def summarize(payload: SummaryRequest):

    try:

        summary = summarize_text(
            payload.text
        )

        return {
            "summary": summary
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )


# -----------------------------
# Learning Path
# -----------------------------

@app.post("/learn/recommendations")
async def learning_path(payload: LearningRequest):

    try:

        recommendations = get_learning_recommendations(
            payload.topic,
            payload.level,
            payload.weeks
        )

        return {
            "recommendations": recommendations
        }

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=str(exc)
        )
