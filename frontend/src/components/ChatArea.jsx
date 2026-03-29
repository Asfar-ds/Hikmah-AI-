import React from "react";
import "../styles/ChatArea.css";
import ChatInput from "./ChatInput"
import ChatMessage from "./ChatMessage";
import { useUser } from '@clerk/clerk-react'
const ChatArea = ({ messages, setMessages, onSend, }) => {
  const { user } = useUser()

  return (
    <div className="chat-area">
      {messages.length === 0 ? (
        <div className="empty-chat">
          <div className="greet">
            <h2>Hello {user?.firstName || "there"}</h2>
            <p>How can I help you?</p>
          </div>
          {/* <div className="questions">
            <span onClick={() => onQuestionClick("What is Riba?")}>What is Riba?</span>
            <span onClick={() => onQuestionClick("Explain Zakat briefly.")}>Explain Zakat briefly.</span>
            <span onClick={() => onQuestionClick("What is Sadaqah?")}>What is Sadaqah?</span>
            <span onClick={() => onQuestionClick("Difference between Riba and Trade.")}>Difference between Riba and Trade.</span>
          </div> */}
        </div>
      ) : (
        messages.map((msg, i) => <ChatMessage key={i} msg={msg} />)
      )
    }
    </div >
  );
};

export default ChatArea;
