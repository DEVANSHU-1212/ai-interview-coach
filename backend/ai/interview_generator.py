async function generateInterview() {
  if (!file) {
    setError("Please upload your resume PDF.");
    return;
  }

  setLoading(true);
  setError("");
  setQuestions([]);
  setFeedback("");
  setAnswer("");
  setFinished(false);
  setCurrentQuestion(0);

  try {
    const formData = new FormData();
    formData.append("file", file);

    const response = await fetch(
      `http://127.0.0.1:8000/generate-interview?role=${encodeURIComponent(role)}`,
      {
        method: "POST",
        body: formData,
      }
    );

    if (!response.ok) {
      throw new Error("Failed to generate interview");
    }

    const data = await response.json();

    if (!data.questions) {
      throw new Error("No questions received");
    }

    // 👇 YAHAN parsing code hai
    const questions = data.questions;

    const questionList = questions
      .split("\n")
      .map((line: string) => line.trim())
      .filter((line: string) => /^\d+\.\s+/.test(line))
      .map((line: string) => line.replace(/^\d+\.\s+/, ""));

    setQuestions(questionList);

  } catch (error) {
    console.error(error);

    setError(
      "Could not connect to the backend. Make sure FastAPI and Ollama are running."
    );
  } finally {
    setLoading(false);
  }
}