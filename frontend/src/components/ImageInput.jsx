import React, { useRef } from "react";
import "../styles/ImageInput.css";

const ImageInput = ({
  image,
  setImage,
  extracting,
  setExtracting,
  extractedText,
  setExtractedText,
  isLoading,
  processImage,
  setError,
}) => {
  const inputRef = useRef(null);

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    processImage(file);
  };

  const handleImageDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    processImage(file);
  };

  return (
    <div
      className="image-drop-area"
      onDrop={handleImageDrop}
      onDragOver={(e) => e.preventDefault()}
    >
      {!image ? (
        <>
          <p>Drop image here, click to select, or paste with Ctrl+V</p>
          <label htmlFor="image-input" className="select-button">
            Select Image
          </label>
        </>
      ) : (
        <div className="image-result">
          <img
            src={URL.createObjectURL(image)}
            alt="Preview"
            className="image-preview"
          />
          {extracting ? (
            <p>Extracting text...</p>
          ) : (
            <p className="extracted-text">Extracted: {extractedText}</p>
          )}
          <button onClick={() => inputRef.current.click()}>Change Image</button>
        </div>
      )}
      <input
        type="file"
        accept="image/*"
        onChange={handleImageChange}
        style={{ display: "none" }}
        id="image-input"
        ref={inputRef}
        disabled={isLoading || extracting}
      />
    </div>
  );
};

export default ImageInput;
