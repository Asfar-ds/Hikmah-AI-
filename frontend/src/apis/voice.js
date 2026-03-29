// import axios from "axios";

// const API_BASE = "http://localhost:8000"; // backend URL

// // Voice file ko text mein convert kare
// export async function sendVoiceToAPI(voiceFile) {
//   try {
//     const formData = new FormData();
//     formData.append("file", voiceFile);

//     const response = await axios({
//       method: "post",
//       url: `${API_BASE}/speech-to-text`,
//       data: formData,
//       headers: {
//         "Content-Type": "multipart/form-data",
//       },
//     });

//     return response.data; // { text: "recognized text" }
//   } catch (err) {
//     console.error("Voice to text error:", err);
//     throw err;
//   }
// }

// // Text ko voice mein convert kare
// export async function getAIResponseVoice(text) {
//   try {
//     const response = await axios({
//       method: "post",
//       url: `${API_BASE}/text-to-speech`,
//       data: { text },
//       responseType: "blob", // backend se audio blob aayega
//     });

//     return response.data; // Blob of audio
//   } catch (err) {
//     console.error("Text to voice error:", err);
//     throw err;
//   }
// }


// export async function sendVoiceToAPI(voiceFile) {
//   const formData = new FormData();
//   formData.append("file", voiceFile);

//   const response = await fetch("http://localhost:8000/speech-to-text", {
//     method: "POST",
//     body: formData
//   });

//   if (!response.ok) {
//     throw new Error("Speech-to-text request failed");
//   }

//   return await response.json();
// }

// export async function getAIResponseVoice(text) {
//   const response = await fetch("http://localhost:8000/text-to-speech", {
//     method: "POST",
//     headers: {
//       "Content-Type": "application/json"
//     },
//     body: JSON.stringify({ text }),
//   });

//   if (!response.ok) {
//     throw new Error("Text-to-speech request failed");
//   }

//   // audio file ko blob mein convert kro
//   const audioBlob = await response.blob();
//   const audioURL = URL.createObjectURL(audioBlob);

//   return audioURL; // is URL ko audio tag mein play kr sakte ho
<<<<<<< HEAD
=======
// const API_BASE = "http://localhost:8000"; // backend URL

// // Speech-to-text
// export async function sendVoiceToAPI(voiceFile) {
//   const formData = new FormData();
//   formData.append("file", voiceFile);

//   try {
//     const res = await fetch(`${API_BASE}/speech-to-text`, {
//       method: "POST",
//       body: formData,
//     });

//     if (!res.ok) throw new Error("Voice to text request failed");
//     const data = await res.json(); // backend { text: "recognized text" }
//     return data;
//   } catch (err) {
//     console.error("Voice to text error:", err.message);
//     throw err;
//   }
// }

// // Text-to-speech
// export async function getAIResponseVoice(text) {
//   try {
//     const res = await fetch(`${API_BASE}/text-to-speech`, {
//       method: "POST",
//       headers: { "Content-Type": "application/json" },
//       body: JSON.stringify({ text }),
//     });

//     if (!res.ok) throw new Error("Text to speech request failed");

//     const blob = await res.blob(); // backend audio blob
//     return blob;
//   } catch (err) {
//     console.error("Text to speech error:", err.message);
//     throw err;
//   }

// }

