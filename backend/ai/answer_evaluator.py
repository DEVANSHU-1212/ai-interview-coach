import requests

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def evaluate_answer(question, answer, role):

    prompt = f"""
You are an expert technical interviewer evaluating a candidate.

Candidate Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the answer carefully.

Give a score from 0 to 10 for each:

Technical Accuracy
Relevance
Clarity
Completeness

Then provide:

Overall Score
Strengths
Weaknesses
Improvement Advice
Better Answer

Use this exact format:

TECHNICAL ACCURACY: X/10
RELEVANCE: X/10
CLARITY: X/10
COMPLETENESS: X/10
OVERALL SCORE: X/10

STRENGTHS:
- point 1
- point 2

WEAKNESSES:
- point 1
- point 2

IMPROVEMENT ADVICE:
- advice 1
- advice 2

BETTER ANSWER:
Write a concise and technically correct improved answer.

Do not use markdown headings.
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

    return {
        "feedback": result["response"]
    }