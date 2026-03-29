export const syncWithBackend = async (idToken, name) => {
  const res = await fetch("http://127.0.0.1:8000/auth/sync", {
    method: "POST",
    headers: {
      Authorization: `Bearer ${idToken}`,
      "Content-Type": "application/json"
    },
    body: JSON.stringify({ name })
  });

  if (!res.ok) {
    const e = await res.json().catch(() => ({}));
    console.log("Backend sync error:", e);
    throw new Error("Sync failed");
  }

  return res.json();
};
