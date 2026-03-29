import { useState, useRef, useEffect } from "react";
import "../styles/ChatInput.css";
import { assets } from "../assets/assets";
// import { sendVoiceToAPI } from "../apis/voice";

const ChatInput = ({ onSend, disabled, suggestion , placeholder }) => {
  const [message, setMessage] = useState("");
  const [showOptions, setShowOptions] = useState(false);
  const [recording, setRecording] = useState(false);
  const [mediaRecorder, setMediaRecorder] = useState(null);

  useEffect(() => {
    if (suggestion) setMessage(suggestion);  // 👈 suggestion aate hi input fill
  }, [suggestion]);

  // Close menu when clicking outside
  useEffect(() => {
    const handleClickOutside = (e) => {
      const menu = document.querySelector(".options-menu");
      const plus = document.querySelector(".plus-icon");
      if (menu && !menu.contains(e.target) && plus && !plus.contains(e.target)) {
        setShowOptions(false);
      }
    };
    document.addEventListener("click", handleClickOutside);
    return () => document.removeEventListener("click", handleClickOutside);
  }, []);



  // Voice recording handler
  const handleRecord = async () => {
    if (recording) {
      mediaRecorder.stop();
      setRecording(false);
      return;
    }

    try {
      const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
      const recorder = new MediaRecorder(stream);
      setMediaRecorder(recorder);
      setRecording(true);

      const chunks = [];
      recorder.ondataavailable = (e) => chunks.push(e.data);

      recorder.onstop = async () => {
        const blob = new Blob(chunks, { type: "audio/webm" });
        const file = new File([blob], "voice_message.webm", { type: "audio/webm" });

        try {
          const result = await sendVoiceToAPI(file);
          onSend(result.text);
        } catch (err) {
          console.error("Voice to text failed:", err);
        }

        stream.getTracks().forEach((track) => track.stop());
      };

      recorder.start();
    } catch (err) {
      console.error("Mic permission error:", err);
    }
  };

  // Form submit
  const handleSubmit = (e) => {
    e.preventDefault();
    if (!message.trim() || disabled) return;
    onSend(message);
    setMessage("");
  };

  // Handle Enter key (without shift)
  const handleEnterKey = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      if (message.trim()) {
        onSend(message);
        setMessage("");
      }
    }
  };

  return (
    <div className="chat-input-container">
      <div className="chat-input-box">
        {/* <div className="plus-icon" onClick={() => setShowOptions(!showOptions)}>
          <img src={assets.plus_icon} alt="plus" />
        </div> */}

        {showOptions && (
          <div className="options-menu">
            {/* Camera */}
            <label className="option-item">
              <img src={assets.camera_icon} alt="camera" />
              <span>Camera</span>
              <input
                type="file"
                accept="image/*"
                capture="environment"
                onChange={(e) =>
                  e.target.files.length > 0 && onSend(e.target.files[0])
                }
              />
            </label>

            {/* Photos */}
            <label className="option-item">
              <img src={assets.photos_icon} alt="photos" />
              <span>Photos</span>
              <input
                type="file"
                accept="image/*"
                onChange={(e) =>
                  e.target.files.length > 0 && onSend(e.target.files[0])
                }
              />
            </label>

            {/* Documents */}
            <label className="option-item">
              <img src={assets.doc_icon} alt="doc" />
              <span>Documents</span>
              <input
                type="file"
                accept=".pdf,.doc,.docx,.txt"
                onChange={(e) =>
                  e.target.files.length > 0 && onSend(e.target.files[0])
                }
              />
            </label>
          </div>
        )}

        {/* Form (textarea + send) */}
        <form onSubmit={handleSubmit} className="input-form">
          {recording ? (
            <div className="recording-wave-animation">
              <span></span><span></span><span></span><span></span>
            </div>
          ) : (
            <input
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              onKeyDown={handleEnterKey}
              placeholder={placeholder}
              disabled={disabled}

            />
          )}

          {/* Voice button */}
          <button
            type="button"
            onClick={handleRecord}
            className={`voice-btn ${recording ? "recording" : ""}`}
            disabled={disabled}
          >
           <img src={assets.mic_icon} alt="mic" />
          </button>
          {/* Send button inside form */}
          <button
            type="submit"
            className="send-btn"
            disabled={disabled || !message.trim()}
          >
            <img src={assets.send_icon} alt="send" />
          </button>
        </form>
      </div>
    </div>
  );
};

export default ChatInput;
