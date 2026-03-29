import React, { useState, useEffect } from "react";
import "../styles/Settings.css";
import { assets } from "../assets/assets";
import { useNavigate } from "react-router-dom";
import { useUser } from "@clerk/clerk-react"


const Settings = () => {
  const [activeTab, setActiveTab] = useState("profile");
  const [darkMode, setDarkMode] = useState(false);
  const [language, setLanguage] = useState("English");
  const navigate = useNavigate();
  const {user , isLoaded } = useUser();
  
  const handleClick = (path) => {
    navigate(path)
  }

  // Dark Mode Handler
  useEffect(() => {
    if (darkMode) {
      document.body.classList.add("dark-mode");
    } else {
      document.body.classList.remove("dark-mode");
    }
  }, [darkMode]);

  // Language Change Handler (simulate translation system)
  const translate = (text) => {
    const translations = {
      Urdu: {
        profile: "پروفائل",
        appearance: "ظاہری شکل",
        language: "زبان",
        darkMode: "ڈارک موڈ",
        currentLanguage: "موجودہ زبان",
      },
      Arabic: {
        profile: "الملف الشخصي",
        appearance: "المظهر",
        language: "اللغة",
        darkMode: "الوضع الداكن",
        currentLanguage: "اللغة الحالية",
      },
      English: {
        profile: "Profile",
        appearance: "Appearance",
        language: "Language",
        darkMode: "Dark Mode",
        currentLanguage: "Current Language",
      },
    };
    return translations[language][text] || text;
  };

  return (
    <div className={`settings-container ${darkMode ? "dark" : ""}`}>
      {/* <Navbar /> */}
      <div className="settings-layout">
        <aside className="settings-sidebar">
          <ul>

            <li
              className="backButton"
              onClick={() => handleClick("/")}
            >
              Home
            </li>
            <li
              className={activeTab === "profile" ? "active" : ""}
              onClick={() => setActiveTab("profile")}
            >
              👤 {translate("profile")}
            </li>
            <li
              className={activeTab === "appearance" ? "active" : ""}
              onClick={() => setActiveTab("appearance")}
            >
              🎨 {translate("appearance")}
            </li>
            <li
              className={activeTab === "language" ? "active" : ""}
              onClick={() => setActiveTab("language")}
            >
              🌐 {translate("language")}
            </li>
          </ul>
        </aside>

        <main className="settings-content">
          {activeTab === "profile" && (
            <div className="tab-content">
              <h2>{translate("profile")}</h2>
              <div className="profile-info">
                <img
                  src={assets.user_icon}
                  alt="User"
                  className="profile-img"
                />
                <div>
                  <p><strong>Name : </strong>{user?.firstName || "Sultan"}</p>
                  <p><strong>Email : </strong>{user?.primaryEmailAddress?.emailAddress || "sultan980123@gmail.com"}</p>
                </div>
              </div>
            </div>
          )}

          {activeTab === "appearance" && (
            <div className="tab-content">
              <h2>{translate("appearance")}</h2>
              <div className="setting-item">
                <label>{translate("darkMode")}</label>
                <input
                  type="checkbox"
                  checked={darkMode}
                  onChange={() => setDarkMode(!darkMode)}
                />
              </div>
            </div>
          )}

          {activeTab === "language" && (
            <div className="tab-content">
              <h2>{translate("language")}</h2>
              <div className="setting-item">
                <label>{translate("language")}</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                >
                  <option value="English">English</option>
                  <option value="Urdu">Urdu</option>
                  <option value="Arabic">Arabic</option>
                </select>
              </div>
              <p className="info">
                {translate("currentLanguage")}: {language}
              </p>
            </div>
          )}
        </main>
      </div>
    </div>
  );
};

export default Settings;
