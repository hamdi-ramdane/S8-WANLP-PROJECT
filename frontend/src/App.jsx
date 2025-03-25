import React, { useState } from "react";
import axios from "axios";
import "./App.css";

function App() {
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const handleSubmit = async () => {
    try {
      const response = await axios.post("http://localhost:5000/predict", {
        text,
      });
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing text:", error);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Fake News Detector (Arabic)</h1>
      <textarea
        className="textarea"
        value={text}
        onChange={(e) => setText(e.target.value)}
        placeholder="Enter Arabic text here..."
      />
      <button className="button" onClick={handleSubmit}>
        Analyze
      </button>
      {result && (
        <div className="result">
          <p className="result-text">Prediction: {result.prediction}</p>
          <p className="result-text">Source Check: {result.source_check}</p>
        </div>
      )}
    </div>
  );
}

export default App;
