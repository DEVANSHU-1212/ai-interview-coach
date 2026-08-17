from fastapi import FastAPI, UploadFile, File
from resume.parser import extract_text_from_pdf
from pydantic import BaseModel
from typing import List
from ai.answer_evaluator import evaluate_answer
from ai.interview_generator import generate_questions
from ai.resume_analyzer import analyze_resume
from ai.question_generator import generate_interview_questions

app = FastAPI(
    title="AI Interview Coach",
    description="AI-powered interview preparation platform",
    version="1.0.0"
)


class InterviewRequest(BaseModel):
    role: str
    experience: str
    skills: List[str]
    difficulty: str
    
class AnswerRequest(BaseModel):
    role: str
    question: str
    answer: str


@app.get("/")
def home():
    return {
        "message": "AI Interview Coach API is running!"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/generate-interview")
def generate_interview(request: InterviewRequest):
    questions = generate_questions(
        request.role,
        request.experience,
        request.skills,
        request.difficulty
    )

    return {
        "role": request.role,
        "experience": request.experience,
        "skills": request.skills,
        "difficulty": request.difficulty,
        "questions": questions
    }

@app.post("/evaluate-answer")
def evaluate_candidate_answer(request: AnswerRequest):

    evaluation = evaluate_answer(
        request.question,
        request.answer,
        request.role
    )

    return {
        "evaluation": evaluation
    }
    
@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    file_path = f"resume/{file.filename}"

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    text = extract_text_from_pdf(file_path)

    return {
        "filename": file.filename,
        "text": text
    }
    
@app.post("/analyze-resume")
async def analyze_uploaded_resume(file: UploadFile = File(...)):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    file_path = f"resume/{file.filename}"

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf(file_path)

    analysis = analyze_resume(resume_text)

    return {
        "filename": file.filename,
        "analysis": analysis
    }
    
@app.post("/generate-interview")
async def generate_interview(
    file: UploadFile = File(...),
    role: str = "AI/ML Engineer"
):

    if not file.filename.lower().endswith(".pdf"):
        return {
            "error": "Only PDF files are supported"
        }

    file_path = f"resume/{file.filename}"

    contents = await file.read()

    with open(file_path, "wb") as f:
        f.write(contents)

    resume_text = extract_text_from_pdf(file_path)

    questions = generate_interview_questions(
        resume_text,
        role
    )

    return {
        "role": role,
        "questions": questions
    }