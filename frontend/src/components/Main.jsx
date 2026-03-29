// import { useState } from "react";
// import '../styles/Main.css';
// import Navbar from "../components/Navbar";
// import ChatArea from "../components/ChatArea";
// import ChatInput from "../components/ChatInput";
// import { analyzeArabicText } from "../apis/arabicService";





// const Main = () => {
//     const [messages, setMessages] = useState([]);
//     const [loading, setLoading] = useState(false);
//     const [isSidebarOpen, setIsSidebarOpen] = useState(false);
//     const toggleSidebar = () => {
//         setIsSidebarOpen(prev => !prev); // پچھلی ویلیو کو الٹ دیتا ہے
//     };
//     const handleSend = async (text) => {
//         try {
//             setLoading(true);
//             // Add user message
//             const userMessage = { sender: "user", text };
//             setMessages(prev => [...prev, userMessage]);

//             // Get Arabic analysis
//             const response = await analyzeArabicText(text);

//             // Add AI response message
//             const aiMessage = { sender: "ai", text: response };
//             setMessages(prev => [...prev, aiMessage]);
//         } catch (error) {
//             console.error("Error analyzing text:", error);
//             // Show error message to user
//             const errorMessage = {
//                 sender: "ai",
//                 text: "Sorry, there was an error analyzing the Arabic text."
//             };
//             setMessages(prev => [...prev, errorMessage]);
//         } finally {
//             setLoading(false);
//         }
//     };

//     const sendMessage = async (msg) => {
//         const token = localStorage.getItem("idToken");

//         const response = await fetch("http://127.0.0.1:8000/fivelens", {
//             method: "POST",
//             headers: {
//                 Authorization: `Bearer ${token}`,
//                 "Content-Type": "application/json"
//             },
//             body: JSON.stringify({ message: msg })
//         });

//         const data = await response.json();
//         console.log(data);
//     };


//     return (
//         <div className="main-right">
//             <Navbar />
//             <div className="chat-layout">
//                 <div className="chat-container">
//                     <ChatArea
//                         messages={messages}
//                         setMessages={setMessages}
//                         onSend={handleSend}
//                         onQuestionClick={setMessages}
//                     />
//                     <ChatInput
//                         onSend={handleSend}
//                         disabled={loading}
//                         messages={messages}
//                         setMessages={setMessages}
//                     />
//                 </div>
//             </div>
//         </div>
//     )
// }

// export default Main
