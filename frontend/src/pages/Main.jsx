import React from "react";
import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import "../styles/Main.css";
import rumi from "../assets/images/rumi.png";

const Main = () => {
  const navigate = useNavigate();

  const fadeInUp = {
    initial: { opacity: 0, y: 20 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.6 },
  };

  return (
    <div className="main-intro">
      <div
        className="bg-image"
        style={{ backgroundImage: `url(${rumi})` }}
        aria-hidden="true"
      />
      <div className="overlay" />

      <motion.div
        className="content"
        initial="initial"
        animate="animate"
        {...fadeInUp}
      >
        <motion.h1
          className="infoName"
          initial={{ scale: 0.9, opacity: 0 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{ duration: 0.8 }}
        >
          Hikmah AI
        </motion.h1>

        <motion.p className="infoP" {...fadeInUp} transition={{ delay: 0.2 }}>
          Hikmah AI is an AI-powered intellectual companion for Dars-e-Nizami
          students. It decodes classical Arabic using a 5-Lens engine, builds a
          relevancy bridge, and helps explore career paths.
        </motion.p>

        <motion.button
          className="cta"
          onClick={() => navigate("/fivelens")}
          whileHover={{ scale: 1.03 }}
          whileTap={{ scale: 0.97 }}
        >
          Start Your Journey
        </motion.button>
          <button
            className="replit-btn start"
            onClick={() => navigate("/opportunity")}
          >
            Start your journey
          </button>
          <button
            className="replit-btn explore"
            onClick={() => navigate("/fivelens")}
          >
            Explore features
          </button>
        </motion.div>

        <motion.div
          className="replit-features"
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.6 }}
        >
          <div className="feature-card">
            <h3>5 Lens Decoder</h3>
            <p>
              Analyze Arabic texts through Sarf, Nahw, Balaghah, Lughat, and
              Urdu synthesis.
            </p>
          </div>

          <div className="feature-card">
            <h3>Relevancy Bridge</h3>
            <p>
              Connect timeless Islamic wisdom with today’s global context and
              challenges.
            </p>
          </div>

          <div className="feature-card">
            <h3>Opportunity Explorer</h3>
            <p>
              Discover career paths that align with Islamic studies and your
              personal goals.
            </p>
          </div>
        </motion.div>
    </div>
  );
};

export default Main;
