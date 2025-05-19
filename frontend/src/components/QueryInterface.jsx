import React, { useState } from "react";
import "./Query.css";

const QueryInterface = () => {
  const [question, setQuestion] = useState("");
  const [response, setResponse] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    setIsLoading(true);
    setError(null);

    try {
      const res = await fetch("http://localhost:5001/api/query", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ question }),
      });

      if (!res.ok) throw new Error("Network response was not ok");

      const data = await res.json();
      setResponse(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="query-container">
      <h1>MedQuery System</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your health records..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? "Processing..." : "Ask"}
        </button>
      </form>

      {error && <div className="error">{error}</div>}

      {response && (
        <div className="response">
          <div className="answer">
            <h3>Answer:</h3>
            <p>{response.answer}</p>
            {response.confidence && (
              <p className="confidence">
                Confidence: {Math.round(response.confidence * 100)}%
              </p>
            )}
          </div>

          {response.data && (
            <div className="data">
              <h3>Supporting Data:</h3>
              <pre>{JSON.stringify(response.data, null, 2)}</pre>
            </div>
          )}
        </div>
      )}

      <div className="examples">
        <h3>Example Questions:</h3>
        <ul>
          <li>What medications am I currently taking?</li>
          <li>When was my last blood test?</li>
          <li>What health events occurred in January 2024?</li>
          <li>How long have I had high cholesterol?</li>
        </ul>
      </div>
    </div>
  );
};

export default QueryInterface;
