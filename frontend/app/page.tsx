"use client";

import { useState } from "react";

type BackendResponse = {
  success?: boolean;
  role?: string;
  filename?: string;
  questions?: unknown;
  detail?: string;
  error?: string;
};

type EvaluationResponse = {
  evaluation?: string | { feedback?: string };
  feedback?: string;
  detail?: string;
  error?: string;
};

export default function Home() {
  const [file, setFile] = useState<File | null>(null);
  const [role, setRole] = useState("AI/ML Engineer");
  const [questions, setQuestions] = useState<string[]>([]);
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [answer, setAnswer] = useState("");
  const [feedback, setFeedback] = useState("");
  const [loading, setLoading] = useState(false);
  const [evaluating, setEvaluating] = useState(false);
  const [error, setError] = useState("");
  const [finished, setFinished] = useState(false);

  async function generateInterview() {
    if (!file) {
      setError("Please upload your resume PDF.");
      return;
    }

    setLoading(true);
    setError("");
    setQuestions([]);
    setCurrentQuestion(0);
    setAnswer("");
    setFeedback("");
    setFinished(false);

    try {
      const formData = new FormData();
      formData.append("file", file);
      formData.append("role", role);

      const response = await fetch(
        "http://127.0.0.1:8000/generate-interview",
        {
          method: "POST",
          body: formData,
        }
      );

      const responseText = await response.text();
      console.log("Generate status:", response.status);
      console.log("Generate response:", responseText);

      let data: BackendResponse;
      try {
        data = JSON.parse(responseText) as BackendResponse;
      } catch {
        throw new Error("Backend returned invalid JSON.");
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.error ||
            `Backend error: ${response.status}`
        );
      }

      if (data.error) {
        throw new Error(data.error);
      }

      let receivedQuestions: string[] = [];

      if (Array.isArray(data.questions)) {
        receivedQuestions = data.questions
          .map((question: unknown) => {
            if (typeof question === "string") {
              return question.trim();
            }

            if (
              typeof question === "object" &&
              question !== null &&
              "question" in question
            ) {
              return String(
                (question as { question: unknown }).question
              ).trim();
            }

            return String(question).trim();
          })
          .filter(Boolean);
      } else if (typeof data.questions === "string") {
        receivedQuestions = data.questions
          .split(/\r?\n/)
          .map((question) =>
            question
              .replace(/^\s*(?:\*\*)?\d+[.)\-:]\s*/, "")
              .replace(/\*\*/g, "")
              .replace(/^[-*]\s*/, "")
              .trim()
          )
          .filter(Boolean);
      }

      console.log("Received questions:", receivedQuestions);
      console.log("Question count:", receivedQuestions.length);

      if (receivedQuestions.length === 0) {
        throw new Error("The backend returned no questions.");
      }

      setQuestions(receivedQuestions);
      setCurrentQuestion(0);
    } catch (error) {
      console.error("Generate interview error:", error);
      setError(
        error instanceof Error
          ? error.message
          : "Could not generate interview questions."
      );
    } finally {
      setLoading(false);
    }
  }

  async function submitAnswer() {
    const currentQuestionText = questions[currentQuestion];

    if (!currentQuestionText) {
      setError("Current question is unavailable.");
      return;
    }

    if (!answer.trim()) {
      setError("Please write your answer first.");
      return;
    }

    setEvaluating(true);
    setError("");
    setFeedback("");

    try {
      const response = await fetch(
        "http://127.0.0.1:8000/evaluate-answer",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            role,
            question: currentQuestionText,
            answer: answer.trim(),
          }),
        }
      );

      const responseText = await response.text();
      console.log("Evaluation status:", response.status);
      console.log("Evaluation response:", responseText);

      let data: EvaluationResponse;
      try {
        data = JSON.parse(responseText) as EvaluationResponse;
      } catch {
        throw new Error("Evaluation backend returned invalid JSON.");
      }

      if (!response.ok) {
        throw new Error(
          data.detail ||
            data.error ||
            `Evaluation failed: ${response.status}`
        );
      }

      let feedbackText = "";

      if (typeof data.evaluation === "string") {
        feedbackText = data.evaluation;
      } else if (
        data.evaluation &&
        typeof data.evaluation.feedback === "string"
      ) {
        feedbackText = data.evaluation.feedback;
      } else if (typeof data.feedback === "string") {
        feedbackText = data.feedback;
      }

      if (!feedbackText.trim()) {
        throw new Error("Backend returned no feedback.");
      }

      setFeedback(feedbackText);
    } catch (error) {
      console.error("Evaluation error:", error);
      setError(
        error instanceof Error
          ? error.message
          : "Could not evaluate your answer."
      );
    } finally {
      setEvaluating(false);
    }
  }

  function nextQuestion() {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion((previous) => previous + 1);
      setAnswer("");
      setFeedback("");
      setError("");
    } else {
      setFinished(true);
    }
  }

  function startNewInterview() {
    setQuestions([]);
    setCurrentQuestion(0);
    setAnswer("");
    setFeedback("");
    setError("");
    setFinished(false);
  }

  if (questions.length === 0 && !finished) {
    return (
      <main className="min-h-screen bg-slate-950 text-white">
        <div className="mx-auto max-w-5xl px-6 py-16">
          <section className="text-center">
            <div className="mb-4 text-5xl">🤖</div>
            <h1 className="text-5xl font-bold">AI Interview Coach</h1>
            <p className="mx-auto mt-5 max-w-2xl text-lg text-slate-400">
              Practice real interviews with AI-powered questions,
              answer evaluation and personalized feedback.
            </p>
          </section>

          <section className="mx-auto mt-12 max-w-2xl rounded-2xl border border-slate-800 bg-slate-900 p-8 shadow-2xl">
            <label className="mb-2 block text-sm font-medium">
              Target Job Role
            </label>

            <select
              value={role}
              onChange={(event) => setRole(event.target.value)}
              className="mb-6 w-full rounded-lg border border-slate-700 bg-slate-800 p-3"
            >
              <option>AI/ML Engineer</option>
              <option>Full Stack Developer</option>
              <option>Backend Developer</option>
              <option>Frontend Developer</option>
              <option>Python Developer</option>
              <option>Software Engineer</option>
            </select>

            <label className="mb-2 block text-sm font-medium">
              Upload Resume
            </label>

            <input
              type="file"
              accept=".pdf,application/pdf"
              onChange={(event) => {
                const selectedFile = event.target.files?.[0] || null;
                setFile(selectedFile);
                setError("");
              }}
              className="mb-4 w-full rounded-lg border border-slate-700 bg-slate-800 p-3 text-sm"
            />

            {file && (
              <p className="mb-4 text-sm text-green-400">✓ {file.name}</p>
            )}

            <button
              type="button"
              onClick={generateInterview}
              disabled={loading}
              className="w-full rounded-lg bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-500 disabled:bg-slate-700"
            >
              {loading ? "Generating Questions..." : "Generate Interview"}
            </button>

            {error && (
              <p className="mt-4 rounded-lg bg-red-950 p-4 text-sm text-red-400">
                {error}
              </p>
            )}
          </section>

          <footer className="mt-16 text-center text-sm text-slate-500">
            Powered by FastAPI • Ollama • Llama 3.2
          </footer>
        </div>
      </main>
    );
  }

  if (finished) {
    return (
      <main className="min-h-screen bg-slate-950 text-white">
        <div className="mx-auto max-w-4xl px-6 py-20 text-center">
          <div className="text-6xl">🎉</div>
          <h1 className="mt-6 text-4xl font-bold">
            Interview Completed!
          </h1>
          <p className="mt-4 text-lg text-slate-400">
            Great job completing your AI interview.
          </p>
          <button
            type="button"
            onClick={startNewInterview}
            className="mt-8 rounded-lg bg-blue-600 px-6 py-3 font-semibold hover:bg-blue-500"
          >
            Start New Interview
          </button>
        </div>
      </main>
    );
  }

  const safeQuestion =
    questions[currentQuestion] || "Question unavailable";
  const progress =
    ((currentQuestion + 1) / questions.length) * 100;

  return (
    <main className="min-h-screen bg-slate-950 text-white">
      <div className="mx-auto max-w-5xl px-6 py-12">
        <section className="text-center">
          <div className="text-5xl">🤖</div>
          <h1 className="mt-4 text-4xl font-bold">
            AI Interview Coach
          </h1>
          <p className="mt-4 text-lg text-slate-400">
            Answer each question like you are in a real interview.
          </p>
        </section>

        <div className="mt-12">
          <div className="mb-4 flex justify-between text-sm text-slate-400">
            <span>
              Question {currentQuestion + 1} of {questions.length}
            </span>
            <span>{Math.round(progress)}%</span>
          </div>

          <div className="h-2 overflow-hidden rounded-full bg-slate-800">
            <div
              className="h-full bg-blue-600 transition-all"
              style={{ width: `${progress}%` }}
            />
          </div>
        </div>

        <section className="mt-10 rounded-2xl border border-slate-800 bg-slate-900 p-8">
          <p className="text-sm font-medium text-blue-400">
            Technical Interview Question
          </p>

          <h2 className="mt-4 text-2xl font-bold leading-relaxed text-white">
            {safeQuestion}
          </h2>

          <label className="mt-10 block text-sm font-medium">
            Your Answer
          </label>

          <textarea
            value={answer}
            onChange={(event) => setAnswer(event.target.value)}
            placeholder="Type your interview answer here..."
            rows={8}
            className="mt-3 w-full resize-none rounded-xl border border-slate-700 bg-slate-800 p-5 text-white outline-none focus:border-blue-500"
          />

          {error && (
            <p className="mt-4 rounded-lg bg-red-950 p-4 text-sm text-red-400">
              {error}
            </p>
          )}

          {!feedback && (
            <button
              type="button"
              onClick={submitAnswer}
              disabled={evaluating || !answer.trim()}
              className="mt-6 w-full rounded-lg bg-blue-600 px-5 py-3 font-semibold hover:bg-blue-500 disabled:bg-slate-700"
            >
              {evaluating
                ? "AI is Evaluating Your Answer..."
                : "Submit Answer"}
            </button>
          )}

          {feedback && (
            <div className="mt-8 rounded-xl border border-slate-700 bg-slate-800 p-6">
              <h3 className="text-xl font-bold text-green-400">
                🤖 AI Feedback
              </h3>
              <div className="mt-5 whitespace-pre-wrap leading-7 text-slate-300">
                {feedback}
              </div>
              <button
                type="button"
                onClick={nextQuestion}
                className="mt-8 w-full rounded-lg bg-green-600 px-5 py-3 font-semibold hover:bg-green-500"
              >
                {currentQuestion < questions.length - 1
                  ? "Next Question →"
                  : "Finish Interview"}
              </button>
            </div>
          )}
        </section>

        <footer className="mt-12 text-center text-sm text-slate-500">
          Powered by FastAPI • Ollama • Llama 3.2
        </footer>
      </div>
    </main>
  );
}