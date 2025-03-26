import React from "react";
import "../styles/Feedback.css";
const Feedback = ({ isLoading, error, result }) => {
  if (isLoading) {
    return (
      <div className="loading-container">
        <div className="spinner"></div>
        <p>Processing your request...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div className="error-container">
        <p className="error-text">{error}</p>
      </div>
    );
  }

  if (result) {
    return (
      <div className="result">
        <p className="result-text">Prediction: {result.prediction}</p>
        <p className="result-text">Source Check: {result.source_check}</p>
      </div>
    );
  }

  return null;
};

export default Feedback;
