// import React from "react";
// import "../styles/ChatMessage.css";
// // import { getAIResponseVoice } from "../apis/voice"; // text-to-speech

// const ChatMessage = ({ msg }) => {
//   useEffect(() => {
//     if (msg.sender === "ai" && msg.text) {
//       const playAIResponse = async () => {
//         try {
//           const audioBlob = await getAIResponseVoice(msg.text);
//           const audioUrl = URL.createObjectURL(audioBlob);
//           const audio = new Audio(audioUrl);
//           audio.play();
//         } catch (err) {
//           console.error("AI voice playback error:", err);
//         }
//       };
//       playAIResponse();
//     }
//   }, [msg]);

//   // Bold formatting for AI messages using **
//   const formatBold = (text) => {
//     if (!text) return null;
//     const regex = /\*\*(.*?)\*\*/g;
//     const result = [];
//     let lastIndex = 0;
//     let match;

//     while ((match = regex.exec(text)) !== null) {
//       if (match.index > lastIndex) {
//         result.push(text.substring(lastIndex, match.index));
//       }
//       result.push(<strong key={lastIndex}>{match[1]}</strong>);
//       lastIndex = match.index + match[0].length;
//     }

//     if (lastIndex < text.length) {
//       result.push(text.substring(lastIndex));
//     }

//     return result;
//   };

//   // Copy message to clipboard
//   const handleCopy = () => {
//     if (msg.text) navigator.clipboard.writeText(msg.text);
//   };

//   // Share message (if supported)
//   const handleShare = () => {
//     if (msg.text && navigator.share) {
//       navigator.share({ text: msg.text }).catch((err) => console.error(err));
//     }
//   };

//   return (
//     <div className={`message-container ${msg.sender}`}>
//       <div className={`message ${msg.sender === "user" ? "user-msg" : "ai-msg"}`}>
//         {msg.text && (
//           <p>{msg.sender === "ai" ? formatBold(msg.text) : msg.text}</p>
//           <p>{msg.sender === "ai" ? formatBold(msg.text) : msg.text}</p>
//         )}
//       </div>

//       {msg.file && (
//         <div className="file-preview">
//           {msg.file.type.startsWith("image/") ? (
//             <img
//               src={typeof msg.file === "string" ? msg.file : URL.createObjectURL(msg.file)}
//               src={URL.createObjectURL(msg.file)}
//               alt="preview"
//               className="preview-img"
//             />
//           ) : (
//             <div className="file-text">
//               <p>{msg.file.name || msg.file}</p>

//               <p>{msg.file.name}</p>
//             </div>
//           )}
//         </div>
//       )}
//       {/* Buttons below message */}
//       <div className={`msg-actions ${msg.sender === "user" ? "right-align" : "left-align"}`}>
//         <div
//           className={`msg-actions ${msg.sender === "user" ? "right-align" : "left-align"
//             }`}>

//           <button onClick={handleCopy}>Copy</button>
//           <button onClick={handleShare}>Share</button>
//         </div>
//       </div>
//     </div>
//     </div >

//   )};

// export default ChatMessage;


// import React, { useEffect } from "react"; // 1. Added useEffect here
// import "../styles/ChatMessage.css";
// // import { getAIResponseVoice } from "../apis/voice"; // Uncomment this if you want voice to work

// const ChatMessage = ({ msg }) => {
//   useEffect(() => {
//     // 2. Added check to ensure function exists before running to prevent crash
//     if (msg.sender === "ai" && msg.text && typeof getAIResponseVoice !== 'undefined') {
//       const playAIResponse = async () => {
//         try {
//           const audioBlob = await getAIResponseVoice(msg.text);
//           const audioUrl = URL.createObjectURL(audioBlob);
//           const audio = new Audio(audioUrl);
//           audio.play();
//         } catch (err) {
//           console.error("AI voice playback error:", err);
//         }
//       };
//       playAIResponse();
//     }
//   }, [msg]);
import React from "react";
import "../styles/ChatMessage.css";

const ChatMessage = ({ msg }) => {

  // Bold formatting for AI messages using **
  const formatBold = (text) => {
    if (!text) return null;
    const regex = /\*\*(.*?)\*\*/g;
    const result = [];
    let lastIndex = 0;
    let match;

    while ((match = regex.exec(text)) !== null) {
      if (match.index > lastIndex) {
        result.push(text.substring(lastIndex, match.index));
      }
      result.push(<strong key={lastIndex}>{match[1]}</strong>);
      lastIndex = match.index + match[0].length;
    }

    if (lastIndex < text.length) {
      result.push(text.substring(lastIndex));
    }

    return result;
  };

  // Copy message to clipboard
  const handleCopy = () => {
    if (msg.text) navigator.clipboard.writeText(msg.text);
  };

  // Share message (if supported)
  const handleShare = () => {
    if (msg.text && navigator.share) {
      navigator.share({ text: msg.text }).catch((err) => console.error(err));
    }
  };

  return (
    <div className={`message-container ${msg.sender}`}>

      <div className={`message ${msg.sender === "user" ? "user-msg" : "ai-msg"}`}>
        {msg.text && (
          <p>{msg.sender === "ai" ? formatBold(msg.text) : msg.text}</p>
        )}
      </div>

      {/* File Preview */}
      {msg.file && (
        <div className="file-preview">
          {msg.file.type && msg.file.type.startsWith("image/") ? (
            <img
              // 3. Fixed duplicate src and added logic for string vs object
              src={typeof msg.file === "string" ? msg.file : URL.createObjectURL(msg.file)}
              alt="preview"
              className="preview-img"
            />
          ) : (
            <div className="file-text">
              <p>{msg.file.name || msg.file}</p>
            </div>
          )}
        </div>
      )}

      {/* Buttons below message */}
      {/* 4. Removed duplicate/nested msg-actions div */}
      {msg.file && (
        <div className="file-preview">
          {msg.file.type.startsWith("image/") ? (
            <img
              src={typeof msg.file === "string" ? msg.file : URL.createObjectURL(msg.file)}
              alt="preview"
              className="preview-img"
            />
          ) : (
            <div className="file-text">
              <p>{msg.file.name || msg.file}</p>
            </div>
          )}
        </div>
      )}
    </div>

  );
};

export default ChatMessage;
