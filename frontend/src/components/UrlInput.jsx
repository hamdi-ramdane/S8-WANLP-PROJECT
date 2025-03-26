import React from "react";
import "../styles/UrlInput.css";
const UrlInput = ({ url, setUrl, isLoading }) => {
  return (
    <input
      type="text"
      className="url-input"
      value={url}
      onChange={(e) => setUrl(e.target.value)}
      placeholder="Enter URL here..."
      disabled={isLoading}
    />
  );
};

export default UrlInput;
