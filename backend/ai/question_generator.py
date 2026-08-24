import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def generate_interview_questions(resume_text: str, role: str):
    prompt = f"""
You are an expert technical interviewer.

Create interview questions for this candidate.

TARGET ROLE:
{role}

CANDIDATE RESUME:
{resume_text}

Generate:

1. 5 Technical Questions
2. 3 Resume/Project Questions
3. 2 Problem-Solving Questions
4. 2 HR/Behavioral Questions

Make the questions relevant to the candidate's resume and target role.

Do not provide answers.
Only provide questions.

Use clear headings and numbered questions.
"""

    try:
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

        data = response.json()

        return data.get(
            "response",
            "No interview questions were generated."
        )

    except requests.exceptions.ConnectionError:
        return "ERROR: Ollama is not running."

    except requests.exceptions.Timeout:
        return "ERROR: Ollama request timed out."

    except Exception as e:
        return f"ERROR: {str(e)}"