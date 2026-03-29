import React from "react";
import { assets } from "../assets/assets";
import "../styles/Navbar.css";
import { useNavigate, useLocation } from "react-router-dom";
import { useUser, useClerk, UserButton } from "@clerk/clerk-react";


const Navbar = ({ toggleSidebar }) => {
  const navigate = useNavigate();
 const location = useLocation(); // <-- useLocation hook is now used correctly
  const path = location.pathname;

  const currentPage = path === "/" ? "" : path.substring(1);

  const { user } = useUser();
  const { openSignIn } = useClerk();

  return (
    <div className="navbar">
      <div className="logo">
        <img
          className="menu"
          src={assets.menu_icon}
          alt="menu"
          onClick={toggleSidebar} // toggle sidebar on click
        />
        <span className="heading" onClick={() => { navigate("/") }}>Hikmah.ai</span>
        <span className="currentPage">{currentPage}</span>
      </div>

      <div className="profile">
        {!user ? (
          <button className="clerk-btn" onClick={openSignIn}>LogIn</button>
        ) : (
          <UserButton />
        )}
      </div>
    </div>
  );
};

export default Navbar;
