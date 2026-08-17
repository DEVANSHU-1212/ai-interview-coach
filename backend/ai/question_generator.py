import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def generate_interview_questions(resume_text, role):

    prompt = f"""
You are an expert technical interviewer.

Create a personalized interview for this candidate.

TARGET JOB ROLE:
{role}

CANDIDATE RESUME:
{resume_text}

Generate exactly:

1. 5 Technical Questions
2. 3 Project-Based Questions
3. 2 HR/Behavioral Questions

Rules:
- Questions must be relevant to the target role.
- Use the candidate's actual skills and projects.
- Do not invent projects or experience.
- Include a mix of easy, medium and difficult questions.
- Make the questions suitable for a real job interview.

Return the questions in this format:

TECHNICAL QUESTIONS:
1.
2.
3.
4.
5.

PROJECT QUESTIONS:
1.
2.
3.

HR QUESTIONS:
1.
2.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=180
    )

    response.raise_for_status()

    return response.json()["response"]