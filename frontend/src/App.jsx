import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Tesseract from "tesseract.js";
import "./App.css";

function App() {
  // Mode selection
  const [mode, setMode] = useState("text");

  // Input states
  const [text, setText] = useState(""); // Text mode
  const [url, setUrl] = useState(""); // URL mode
  const [image, setImage] = useState(null); // Image mode
  const [extracting, setExtracting] = useState(false); // Image extraction status
  const [extractedText, setExtractedText] = useState(""); // Extracted text from image
  const [voiceText, setVoiceText] = useState(""); // Voice mode
  const [recording, setRecording] = useState(false); // Voice recording status

  // Result and feedback states
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Refs for voice recognition and image input
  const recognitionRef = useRef(null);
  const timeoutRef = useRef(null);
  const inputRef = useRef(null); // For image input

  // Initialize SpeechRecognition
  useEffect(() => {
    if ("SpeechRecognition" in window || "webkitSpeechRecognition" in window) {
      const SpeechRecognition =
        window.SpeechRecognition || window.webkitSpeechRecognition;
      recognitionRef.current = new SpeechRecognition();
      recognitionRef.current.lang = "ar"; // Arabic
      recognitionRef.current.interimResults = false;
      recognitionRef.current.onresult = (event) => {
        const transcript = event.results[0][0].transcript;
        setVoiceText(transcript);
        if (!isLoading) handleSubmit(transcript); // Auto-send after recording
      };
      recognitionRef.current.onend = () => {
        setRecording(false);
        if (timeoutRef.current) {
          clearTimeout(timeoutRef.current);
          timeoutRef.current = null;
        }
      };
      recognitionRef.current.onerror = (event) =>
        setError("Speech recognition error: " + event.error);
    } else {
      setError("Speech recognition not supported in this browser.");
    }
  }, [isLoading]);

  // Handle paste event for image mode
  useEffect(() => {
    const handlePaste = (e) => {
      if (mode === "image" && !extracting) {
        const items = e.clipboardData.items;
        for (let i = 0; i < items.length; i++) {
          if (items[i].type.indexOf("image") !== -1) {
            const blob = items[i].getAsFile();
            processImage(blob);
            break;
          }
        }
      }
    };

    document.addEventListener("paste", handlePaste);
    return () => {
      document.removeEventListener("paste", handlePaste);
    };
  }, [mode, extracting]);

  // Image handling
  const handleImageChange = (e) => {
    const file = e.target.files[0];
    processImage(file);
  };

  const handleImageDrop = (e) => {
    e.preventDefault();
    const file = e.dataTransfer.files[0];
    processImage(file);
  };

  const processImage = (file) => {
    if (file && !extracting) {
      setImage(file);
      setExtracting(true);
      setExtractedText("");
      Tesseract.recognize(file, "ara")
        .then(({ data: { text } }) => {
          setExtractedText(text);
          setExtracting(false);
        })
        .catch((err) => {
          setError("Failed to extract text from image.");
          setExtracting(false);
        });
    }
  };

  // Voice handling
  const handleVoiceRecording = () => {
    if (!recording && !isLoading && recognitionRef.current) {
      recognitionRef.current.start();
      setRecording(true);
      timeoutRef.current = setTimeout(() => {
        recognitionRef.current.stop();
      }, 10000); // 10-second max
    }
  };

  // Submit handler
  const handleSubmit = async (overrideText = null) => {
    let textToSend;
    switch (mode) {
      case "text":
        textToSend = text;
        break;
      case "url":
        textToSend = url;
        break;
      case "image":
        textToSend = extractedText;
        break;
      case "voice":
        textToSend = overrideText || voiceText; // Use override for auto-send
        break;
      default:
        textToSend = "";
    }

    if (!textToSend) {
      setError("Please provide input to analyze.");
      return;
    }

    try {
      setIsLoading(true);
      setError(null);
      setResult(null);
      const response = await axios.post("http://localhost:5000/predict", {
        text: textToSend,
      });
      setResult(response.data);
    } catch (error) {
      if (error.response) {
        setError(
          `Server error: ${error.response.status} - ${
            error.response.data.message || "Unknown error"
          }`
        );
      } else if (error.request) {
        setError("Network error: Unable to reach the server");
      } else {
        setError(`Error: ${error.message}`);
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="container">
      <h1 className="title">Fake News Detector (Arabic)</h1>

      {/* Mode Selection */}
      <div className="mode-selection">
        <button
          onClick={() => setMode("text")}
          className={mode === "text" ? "active" : ""}
        >
          Text
        </button>
        <button
          onClick={() => setMode("image")}
          className={mode === "image" ? "active" : ""}
        >
          Image
        </button>
        <button
          onClick={() => setMode("url")}
          className={mode === "url" ? "active" : ""}
        >
          URL
        </button>
        <button
          onClick={() => setMode("voice")}
          className={mode === "voice" ? "active" : ""}
        >
          Voice
        </button>
      </div>

      {/* Input Area */}
      <div className="input-container">
        {mode === "text" && (
          <textarea
            className="textarea"
            value={text}
            onChange={(e) => setText(e.target.value)}
            placeholder="Enter Arabic text here..."
            disabled={isLoading}
          />
        )}
        {mode === "image" && (
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
                <button onClick={() => inputRef.current.click()}>
                  Change Image
                </button>
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
        )}
        {mode === "url" && (
          <input
            type="text"
            className="url-input"
            value={url}
            onChange={(e) => setUrl(e.target.value)}
            placeholder="Enter URL here..."
            disabled={isLoading}
          />
        )}
        {mode === "voice" && (
          <div className="voice-input">
            <button
              className="button"
              onClick={handleVoiceRecording}
              disabled={recording || isLoading}
            >
              {recording ? "Recording..." : "Record Voice (10s max)"}
            </button>
            {voiceText && (
              <p className="transcribed-text">Transcribed: {voiceText}</p>
            )}
          </div>
        )}
      </div>

      {/* Analyze Button (hidden for voice mode as it auto-sends) */}
      {mode !== "voice" && (
        <button
          className="button"
          onClick={() => handleSubmit()}
          disabled={isLoading}
        >
          {isLoading ? "Analyzing..." : "Analyze"}
        </button>
      )}

      {/* Feedback */}
      {isLoading && (
        <div className="loading-container">
          <div className="spinner"></div>
          <p>Processing your request...</p>
        </div>
      )}
      {error && !isLoading && (
        <div className="error-container">
          <p className="error-text">{error}</p>
        </div>
      )}
      {result && !isLoading && !error && (
        <div className="result">
          <p className="result-text">Prediction: {result.prediction}</p>
          <p className="result-text">Source Check: {result.source_check}</p>
        </div>
      )}
    </div>
  );
}

export default App;
