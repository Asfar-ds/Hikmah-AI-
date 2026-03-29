// // const API_URL = '/apis';

// // ✅ Vite Environment Variable way
// const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// // Usage example
// // fetch(`${BASE_URL}/analyze-arabic`)

// export const analyzeArabicText = async (text, language = 'Urdu and English') => {
//     try {
//         console.log('Calling Arabic analysis API with:', { text, language });
//         const response = await fetch(`${BASE_URL}/analyze-arabic`, {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/json',
//             },
//             body: JSON.stringify({
//                 text: text,
//                 language: language
//             })
//         });

//         console.log('Arabic API response status:', response.status);
//         if (!response.ok) {
//             const errorData = await response.json();
//             console.error('Arabic API error:', errorData);
//             throw new Error(errorData.detail || 'Failed to analyze Arabic text');
//         }

//         const data = await response.json();
//         return data.explanation;
//     } catch (error) {
//         console.error('Arabic service error:', error);
//         throw error;
//     }
// };

// from uploaded:arabicService.js (corrected version)

const BASE_URL = 'https://hikmah-backend-production.up.railway.app';  // always safe because Nginx proxies it
// const API_URL = 'http://localhost:8000'; // For local testing reference

export const analyzeArabicText = async (text, language = 'Urdu') => {

    // Choose which URL to use for the API call (BASE_URL for Docker)
    // const apiUrlToUse = BASE_URL; 

    try {
        console.log('Calling Arabic analysis API with:', { text, language });

        // FIX: Added the '/fivelens' prefix to match the FastAPI router defined in main.py
        const response = await fetch(`${BASE_URL}/analyze-arabic/analyze-arabic`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                text: text,
                language: language
            })
        });

        // ... rest of the function ...

        console.log('Arabic API response status:', response.status);
        if (!response.ok) {
            const errorData = await response.json();
            console.error('Arabic API error:', errorData);
            throw new Error(errorData.detail || 'Failed to analyze Arabic text');
        }

        const data = await response.json();
        return data.explanation;
    } catch (error) {
        console.error('Arabic service error:', error);
        throw error;
    }
};
