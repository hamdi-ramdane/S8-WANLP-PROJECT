import React, { useState, useRef, useEffect } from "react";
import axios from "axios";
import Tesseract from "tesseract.js";
import ModeSelector from "./components/ModeSelector";
import TextInput from "./components/TextInput";
import ImageInput from "./components/ImageInput";
import UrlInput from "./components/UrlInput";
import VoiceInput from "./components/VoiceInput";
import AnalyzeButton from "./components/AnalyzeButton";
import Feedback from "./components/Feedback";
import "./App.css";

function App() {
  // Mode selection
  const [mode, setMode] = useState("text");

  // Input states
  const [text, setText] = useState("");
  const [url, setUrl] = useState("");
  const [image, setImage] = useState(null);
  const [extracting, setExtracting] = useState(false);
  const [extractedText, setExtractedText] = useState("");
  const [voiceText, setVoiceText] = useState("");
  const [recording, setRecording] = useState(false);

  // Result and feedback states
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // Refs for voice recognition
  const recognitionRef = useRef(null);
  const timeoutRef = useRef(null);

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
        if (!isLoading) handleSubmit(transcript); // Auto-submit after recording
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

    if (mode === "image") {
      document.addEventListener("paste", handlePaste);
    }

    return () => {
      document.removeEventListener("paste", handlePaste);
    };
  }, [mode, extracting]);

  // Image processing
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
        textToSend = overrideText || voiceText;
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

      <ModeSelector currentMode={mode} setMode={setMode} />

      <div className="input-container">
        {mode === "text" && (
          <TextInput text={text} setText={setText} isLoading={isLoading} />
        )}
        {mode === "image" && (
          <ImageInput
            image={image}
            setImage={setImage}
            extracting={extracting}
            setExtracting={setExtracting}
            extractedText={extractedText}
            setExtractedText={setExtractedText}
            isLoading={isLoading}
            processImage={processImage}
            setError={setError}
          />
        )}
        {mode === "url" && (
          <UrlInput url={url} setUrl={setUrl} isLoading={isLoading} />
        )}
        {mode === "voice" && (
          <VoiceInput
            voiceText={voiceText}
            recording={recording}
            handleVoiceRecording={handleVoiceRecording}
            isLoading={isLoading}
          />
        )}
      </div>

      {mode !== "voice" && (
        <AnalyzeButton isLoading={isLoading} handleSubmit={handleSubmit} />
      )}

      <Feedback isLoading={isLoading} error={error} result={result} />
    </div>
  );
}

export default App;
