from fastapi import FastAPI
from pydantic import BaseModel
from backend.agent import (
    extract_skills,
    generate_questions,
    evaluate_answer,
    generate_learning_plan
)
from backend.scoring import calculate_final_score, identify_gaps
from fastapi import UploadFile, File
from backend.utils import extract_text_from_pdf, extract_text_from_docx


app = FastAPI()

class InputData(BaseModel):
    jd: str
    resume: str

@app.post("/upload-resume")
async def upload_resume(file: UploadFile = File(...)):
    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)

    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file.file)

    else:
        return {"error": "Unsupported file format"}

    text = text[:2000]  # limit

    return {
        "resume_text": text[:1000]
    }


@app.post("/analyze")
def analyze(data: InputData):
    jd_text = data.jd[:1000]
    resume_text = data.resume[:1000]

    jd_skills = extract_skills(jd_text)
    resume_skills = extract_skills(resume_text)
    print("JD length:", len(data.jd))
    print("Resume length:", len(data.resume))

    return {
        "jd_skills": jd_skills,
        "resume_skills": resume_skills
    }


@app.post("/questions")
def questions(skill: str):
    return {"questions": generate_questions(skill)}


@app.post("/evaluate")
def evaluate(skill: str, answer: str):
    return {"result": evaluate_answer(skill, answer)}


@app.post("/final-report")
def final_report(scores: dict):
    print("DEBUG SCORES:", scores)
    final_score = calculate_final_score(scores)
    gaps = identify_gaps(scores)
    roadmap = generate_learning_plan(gaps)

    return {
        "final_score": final_score,
        "gaps": gaps,
        "learning_plan": roadmap
    }
