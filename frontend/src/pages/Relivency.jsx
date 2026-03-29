import { useState } from "react";
import '../styles/agents.css';
import Navbar from "../components/Navbar";
import ChatArea from "../components/ChatArea";
import ChatInput from "../components/ChatInput";
import Sidebar from "../components/Sidebar";
import { sendChatMessage } from "../apis/chatService";
// Example: Add this line to the top of your JSX files
// import { getAIResponseVoice } from "./apis/voice.js"; // Adjust path as necessary


const Relivency = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false);

  const toggleSidebar = () => {
    setOpen(prev => !prev);
  };

  const handleSend = async (text) => {
    try {
      setLoading(true);
      // Add user message
      const userMessage = { sender: "user", text };
      setMessages(prev => [...prev, userMessage]);

      // Get AI response
      const response = await sendChatMessage(text);

      // Add AI message
      const aiMessage = { sender: "ai", text: response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error sending message:", error);
      // Show error message to user
      const errorMessage = { sender: "ai", text: "Sorry, there was an error processing your message." };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };


  return (
    <div className="main" style={{ background: `linear-gradient(to top ,rgba(6,148,84, 0.6), #ffffff)` }}>
      <Sidebar open={open}
        setOpen={setOpen} />
      {open && (
        <div
          className="fixed inset-0 bg-[#bbbaba7a] bg-opacity-50 z-40 md:hidden"
          onClick={() => setOpen(false)}
        ></div>)}
      <div className="right">
        <Navbar toggleSidebar={toggleSidebar} />
        <div className="chat-layout">
          <div className="chat-container">
            <ChatArea messages={messages} />
            <ChatInput
              onSend={handleSend}
              disabled={loading}
              placeholder="Describe your interests"
            />
            <p style={{ fontFamily: "monospace", color: `rgba(255,255,255,0.5)` }}>Lorem ipsum dolor sit amet.</p>

          </div>
        </div>
      </div>

    </div>
  );
};

export default Relivency
