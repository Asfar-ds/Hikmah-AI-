// // const API_URL = "http://localhost:8000"; // same as your FastAPI base
// // const API_URL = '/apis';

// // ✅ Vite Environment Variable way
// const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

// // Usage example
// // fetch(`${BASE_URL}/opportunities`)


// export const getJobOpportunities = async (profile) => {
//   try {
//     const payload = {
//       interests: profile.interests || "",
//       background: profile.background || "",
//     };

//     console.log("Sending payload to backend:", payload);

//     const response = await fetch(`${BASE_URL}/opportunities`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(payload),
//     });

//     const data = await response.json();

//     if (!response.ok) {
//       console.error("Backend error:", data);
//       throw new Error(data.detail || "Failed to get opportunities");
//     }

//     console.log("Backend response:", data);
//     return data.response || data.received; // to support your test route
//   } catch (error) {
//     console.error("API Error:", error);
//     throw error;
//   }
// };

// export const getSkillsetForJob = async (jobSelection) => {
//   try {
//     const payload = {
//       job_title: jobSelection.job_title || "",
//     };

//     console.log("Sending payload to backend:", payload);

//     const response = await fetch(`${API_URL}/skillset`, {
//       method: "POST",
//       headers: {
//         "Content-Type": "application/json",
//       },
//       body: JSON.stringify(payload),
//     });

//     const data = await response.json();

//     if (!response.ok) {
//       console.error("Backend returned error:", data);
//       throw new Error(data.detail || "Failed to get skillset");
//     }

//     console.log("Response from backend:", data);
//     return data.response || data.received;
//   } catch (error) {
//     console.error("Error:", error);
//     throw error;
//   }
// };


// ✅ Vite Environment Variable way
// const BASE_URL = import.meta.env.VITE_API_URL || "http://localhost:8000"; 
const API_URL = "https://hikmah-backend-production.up.railway.app"
export const getJobOpportunities = async (profile) => {
  try {
    const payload = {
      interests: profile.interests || "",
      background: profile.background || "",
    };

    console.log("Sending payload to backend:", payload);

    const response = await fetch(`${API_URL}/opportunities`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Backend error:", data);
      throw new Error(data.detail || "Failed to get opportunities");
    }

    console.log("Backend response:", data);
    return data.response || data.received;

  } catch (error) {
    console.error("API Error:", error);
    throw error;
  }
};

export const getSkillsetForJob = async (jobSelection) => {
  try {
    const payload = {
      job_title: jobSelection.job_title || "",
    };

    console.log("Sending payload to backend:", payload);

    // ✅ FIXED: Changed API_URL to BASE_URL
    const response = await fetch(`${BASE_URL}/skillset`, {

      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    });

    const data = await response.json();

    if (!response.ok) {
      console.error("Backend returned error:", data);
      throw new Error(data.detail || "Failed to get skillset");
    }

    console.log("Response from backend:", data);
    return data.response || data.received;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}