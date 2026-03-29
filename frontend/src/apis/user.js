export const getUserProfile = async () => {
  const token = localStorage.getItem("idToken");

  return fetch("http://127.0.0.1:8000/user_profile", {
    headers: { Authorization: `Bearer ${token}` }
  }).then(res => res.json());
};
