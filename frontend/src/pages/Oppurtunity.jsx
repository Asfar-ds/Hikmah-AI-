import { useState } from "react";
import '../styles/agents.css';
import Navbar from "../components/Navbar";
import ChatArea from "../components/ChatArea";
import ChatInput from "../components/ChatInput";
import Sidebar from "../components/Sidebar";
import { getJobOpportunities } from "../apis/opportunityService";
// import { getAIResponseVoice } from "./apis/voice.js"; // Adjust path as necessary


const Opportunity = () => {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [open, setOpen] = useState(false)

  const toggleSidebar = () => {
    setOpen(prev => !prev);
  };

  const handleSend = async (text) => {
    try {
      setLoading(true);
      // Add user message
      const userMessage = { sender: "user", text };
      setMessages(prev => [...prev, userMessage]);

      // Create profile from user input
      const profile = {
        interests: text
      };


      // Get opportunities
      const response = await getJobOpportunities(profile);

      // Add AI response message
      const aiMessage = { sender: "ai", text: response };
      setMessages(prev => [...prev, aiMessage]);
    } catch (error) {
      console.error("Error getting opportunities:", error);
      // Show error message to user
      const errorMessage = {
        sender: "ai",
        text: "Sorry, there was an error finding opportunities."
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const sendMessage = async (msg) => {
    const token = localStorage.getItem("idToken");

    const response = await fetch("http://127.0.0.1:8000/opportunity", {
      method: "POST",
      headers: {
        Authorization: `Bearer ${token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ message: msg })
    });

    const data = await response.json();
    console.log(data);
  };

  return (
    <div className="main" style={{ background: `linear-gradient(to top ,rgba(2,148,104, 0.6), #ffffff)` }}>
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
              placeholder={"Describe your skills..."}
            />
            <p style={{ fontFamily: "monospace", color: `rgba(255,255,255,0.5)` }}>Lorem ipsum dolor sit amet.</p>

          </div>
        </div>
      </div>

    </div>
  );
};

export default Opportunity;
