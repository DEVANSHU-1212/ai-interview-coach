import requests


OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "llama3.2"


def evaluate_answer(question, answer, role):

    prompt = f"""
You are an expert technical interviewer.

Candidate Role:
{role}

Interview Question:
{question}

Candidate Answer:
{answer}

Evaluate the candidate's answer.

Give scores from 0 to 10 for:

1. Technical Accuracy
2. Relevance
3. Clarity
4. Completeness

Also provide:

- Overall Score
- Strengths
- Weaknesses
- Improvement Advice
- Better Answer

Return the evaluation in a clear structured format.
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