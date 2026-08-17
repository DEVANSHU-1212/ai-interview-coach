import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def analyze_resume(resume_text):

    prompt = f"""
You are an expert AI resume analyzer and technical recruiter.

Analyze the following resume:

---------------- RESUME ----------------

{resume_text}

-------------- END RESUME --------------

Extract the following information:

1. Candidate Name
2. Education
3. Technical Skills
4. Programming Languages
5. Frameworks and Libraries
6. Tools and Technologies
7. Projects
8. Work Experience
9. Certifications
10. Strengths
11. Weak Areas
12. Recommended Job Roles

Give the result in a clear structured format.

Do not invent information that is not present in the resume.
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

    result = response.json()

    return result["response"]