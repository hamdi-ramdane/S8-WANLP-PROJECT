import React from "react";
import "../styles/AnalyzeButton.css";
const AnalyzeButton = ({ isLoading, handleSubmit }) => {
  return (
    <button className="button" onClick={handleSubmit} disabled={isLoading}>
      {isLoading ? "Analyzing..." : "Analyze"}
    </button>
  );
};

export default AnalyzeButton;
