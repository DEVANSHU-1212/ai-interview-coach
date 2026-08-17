import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def generate_questions(role, experience, skills, difficulty):

    skills_text = ", ".join(skills)

    prompt = f"""
You are an expert technical interviewer.

Create 5 interview questions for:

Job Role: {role}
Experience Level: {experience}
Skills: {skills_text}
Difficulty: {difficulty}

Requirements:

- Questions must be relevant to the job role.
- Include technical questions.
- Include practical/problem-solving questions.
- Include questions based on the candidate's skills.
- Avoid repetitive questions.

Return exactly 5 questions numbered 1 to 5.
"""

    response = requests.post(
        OLLAMA_URL,
        json={
            "model": MODEL,
            "prompt": prompt,
            "stream": False
        },
        timeout=120
    )

    response.raise_for_status()

    result = response.json()

    return result["response"]