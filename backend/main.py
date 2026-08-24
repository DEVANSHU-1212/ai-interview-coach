from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
import re

from resume.parser import extract_text_from_pdf
from ai.answer_evaluator import evaluate_answer
from ai.resume_analyzer import analyze_resume
from ai.question_generator import generate_interview_questions


app = FastAPI(
    title="AI Interview Coach",
    description="AI-powered interview preparation platform",
    version="1.0.0"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# Request Models
# ============================================================

class AnswerRequest(BaseModel):
    role: str
    question: str
    answer: str


# ============================================================
# Home
# ============================================================

@app.get("/")
def home():
    return {
        "message": "AI Interview Coach API is running!",
        "version": "1.0.0"
    }


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


# ============================================================
# Evaluate Interview Answer
# ============================================================

@app.post("/evaluate-answer")
def evaluate_candidate_answer(request: AnswerRequest):

    evaluation = evaluate_answer(
        request.question,
        request.answer,
        request.role
    )

    return {
        "role": request.role,
        "question": request.question,
        "answer": request.answer,
        "evaluation": evaluation
    }


# ============================================================
# Upload Resume
# ============================================================

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename:
        return {
            "error": "No file selected"
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    os.makedirs("resume", exist_ok=True)

    file_path = os.path.join(
        "resume",
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    text = extract_text_from_pdf(file_path)

    return {
        "success": True,
        "filename": file.filename,
        "text": text
    }


# ============================================================
# Analyze Resume
# ============================================================

@app.post("/analyze-resume")
async def analyze_uploaded_resume(
    file: UploadFile = File(...)
):

    if not file.filename:
        return {
            "error": "No file selected"
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    os.makedirs("resume", exist_ok=True)

    file_path = os.path.join(
        "resume",
        file.filename
    )

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf(file_path)

    analysis = analyze_resume(resume_text)

    return {
        "success": True,
        "filename": file.filename,
        "analysis": analysis
    }


# ============================================================
# Generate Interview Questions
# ============================================================

from fastapi import File, Form, UploadFile

@app.post("/generate-interview")
async def generate_interview(
    file: UploadFile = File(...),
    role: str = Form(...)
):
    if not file.filename:
        return {
            "error": "No resume file selected"
        }

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    os.makedirs("resume", exist_ok=True)

    file_path = os.path.join(
        "resume",
        os.path.basename(file.filename)
    )

    contents = await file.read()

    with open(file_path, "wb") as saved_file:
        saved_file.write(contents)

    resume_text = extract_text_from_pdf(file_path)

    if not resume_text.strip():
        return {
            "error": "Could not extract text from the resume"
        }

    questions = generate_interview_questions(
        resume_text,
        role
    )

    if isinstance(questions, str):
        questions = [
            line.strip()
            for line in questions.splitlines()
            if line.strip()
        ]

    return {
        "success": True,
        "role": role,
        "questions": questions
    }