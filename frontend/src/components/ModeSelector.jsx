import React from "react";
import "../styles/ModeSelector.css";
const ModeSelector = ({ currentMode, setMode }) => {
  return (
    <div className="mode-selection">
      <button
        onClick={() => setMode("text")}
        className={currentMode === "text" ? "active" : ""}
      >
        Text
      </button>
      <button
        onClick={() => setMode("image")}
        className={currentMode === "image" ? "active" : ""}
      >
        Image
      </button>
      <button
        onClick={() => setMode("url")}
        className={currentMode === "url" ? "active" : ""}
      >
        URL
      </button>
      <button
        onClick={() => setMode("voice")}
        className={currentMode === "voice" ? "active" : ""}
      >
        Voice
      </button>
    </div>
  );
};

export default ModeSelector;
