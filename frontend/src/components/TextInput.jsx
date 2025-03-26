import React from "react";
import "../styles/TextInput.css";
const TextInput = ({ text, setText, isLoading }) => {
  return (
    <textarea
      className="textarea"
      value={text}
      onChange={(e) => setText(e.target.value)}
      placeholder="Enter Arabic text here..."
      disabled={isLoading}
    />
  );
};

export default TextInput;
