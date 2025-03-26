import React from "react";
import "../styles/VoiceInput.css";

const VoiceInput = ({
  voiceText,
  recording,
  handleVoiceRecording,
  isLoading,
}) => {
  return (
    <div className="voice-input">
      <button
        className="button"
        onClick={handleVoiceRecording}
        disabled={recording || isLoading}
      >
        {recording ? "Recording..." : "Record Voice"}
      </button>
      {voiceText && (
        <p className="transcribed-text">Transcribed: {voiceText}</p>
      )}
    </div>
  );
};

export default VoiceInput;
