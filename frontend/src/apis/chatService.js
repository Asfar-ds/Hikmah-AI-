// const API_URL = 'http://localhost:8000';

// const BASE_URL = "/api"; // always safe because Nginx proxies it
// export const sendChatMessage = async (message, language = 'Urdu') => {
//     try {
//         // ✅ FIXED: Changed API_URL to BASE_URL
//         const response = await fetch(`${BASE_URL}/chat`, {
//             export const sendChatMessage = async (message, language = 'Urdu') => {
//                 try {
//                     const response = await fetch(`${API_URL}/chat`, {
//                         method: 'POST',
//                         headers: {
//                             'Content-Type': 'application/json',
//                         },
//                         body: JSON.stringify({
//                             user_input: message,
//                             language: language
//                         })
//                     });

//                     if (!response.ok) {
//                         throw new Error('Network response was not ok');
//                     }

//                     const data = await response.json();
//                     return data.response;
//                 } catch (error) {
//                     console.error('Error:', error);
//                     throw error;
//                 }
//             };

//         };

// const API_URL = 'http://localhost:8000'; // Note: API_URL is still defined but not used in the fixed function.
const BASE_URL = 'https://hikmah-backend-production.up.railway.app'; // always safe because Nginx proxies it

export const sendChatMessage = async (user_input ,language = 'Urdu') => {
    try {
        const response = await fetch(`${BASE_URL}/chat/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_input: user_input,
                language  : language 
            })
        });

        if (!response.ok) {
            // Throw a more informative error including the status
            throw new Error(`Network response was not ok. Status: ${response.status}`);
        }

        const data = await response.json();
        return data.response;
    } catch (error) {
        console.error('Error in sendChatMessage:', error);
        throw error;
    }
};
