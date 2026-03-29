import React, { useEffect, useRef, useState } from "react";
import { motion } from "framer-motion";
import '../styles/Home.css';
import { useNavigate } from "react-router-dom";
import { siteCopy } from "../lib/copy"
import { assets } from "../assets/assets";

const Home = () => {

  const navigate = useNavigate();

  const lensRef = useRef(null);
  const relevancyRef = useRef(null);
  const opportunityRef = useRef(null);

  const scrollToSection = (ref) => {
    ref.current?.scrollIntoView({ behavior: "smooth" });}


    const fadeIn = {
      initial: { opacity: 0, y: 20 },
      whileInView: { opacity: 1, y: 0 },
      viewport: { once: true },
      transition: { duration: 0.6 }
    };
  
  return (
    <div className="homePage">
      <nav className="nav">
        <div className="home-logo">
          {/* <Scroll className="icon" /> */}
          <h1>Hikmah.ai</h1>
        </div>
        <div className="nav-links">
          <a onClick={() => scrollToSection(lensRef)}>The 5-Lens Decorator</a>
          <a onClick={() => scrollToSection(relevancyRef)}>The Relevancy Bridge</a>
          <a onClick={() => scrollToSection(opportunityRef)}>Career Paths</a>
        </div>
        <button className="btn btn-primary" onClick={()=>{navigate("/fivelens")}}>
          Start Learning
        </button>
      </nav>

      <section className="hero">
        <div className="hero-bg "></div>
        <div className="fade"></div>
        <div className="hero-content">
          <motion.div
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <span className="badge">
              Knowledge Reshapes Tomorrow
            </span>
            <h1 className="hero-title">
              Where Tradition Meets <br />
              <span className="gradient-text">Transformation</span>
            </h1>
            <p className="hero-subtitle">
              Empowering the scholars of today with the technology of tomorrow.
              Hikmah AI bridges the gap between sacred texts and modern intellect.
            </p>
            <div className="hero-actions">
              <button className="btn btn-lg btn-primary" onClick={()=>{navigate("/fivelens")}}>
                Explore the Platform
              </button>
              <button className="btn btn-lg btn-outline">
                Learn More
              </button>
            </div>
          </motion.div>
        </div>
      </section>

      <section id="decorator" className="section" ref={lensRef}>
        <div className="container">
          <div className="grid-2">
            <motion.div {...fadeIn} className="image-col">
              <div className="image-wrapper">
                <img
                  src={assets.fivelens}
                  alt="Linguistic Analysis Layers"
                />
                <div className="image-overlay" />
              </div>
              <div className="meta-info">
                <div className="meta-box">
                  "{siteCopy.section1.refinements.poetic}"
                </div>
              </div>
            </motion.div>

            <motion.div {...fadeIn} className="text-col">
              <div className="section-header">
                {/* <Layers className="icon-accent" /> */}
                <span className="overline">The 5-Lens Decorator</span>
              </div>
              <h2 className="section-title">
                {siteCopy.section1.headline}
              </h2>
              <h3 className="section-subtitle">
                {siteCopy.section1.subheading}
              </h3>
              <p className="section-text">
                {siteCopy.section1.paragraph}
              </p>

              <ul className="feature-list">
                {siteCopy.section1.bullets.map((item, i) => (
                  <li key={i}>
                    <span className="dot" />
                    {item}
                  </li>
                ))}
              </ul>

              <div className="highlight-box">
                <p>
                  {siteCopy.section1.purpose}
                </p>
              </div>
            </motion.div>
          </div>
        </div>
      </section>


      {/* Section 2: The Relevancy Bridge */}
      <section id="bridge" className="section bg-muted" ref={relevancyRef}>
        <div className="container">
          <div className="grid-2">
            <motion.div {...fadeIn}>
              <div className="section-header">
                {/* <Network className="icon-accent" /> */}
                <span className="overline">The Relevancy Bridge</span>
              </div>
              <h2 className="section-title">
                {siteCopy.section2.headline}
              </h2>
              <h3 className="section-subtitle">
                {siteCopy.section2.subheading}
              </h3>
              <p className="section-text">
                {siteCopy.section2.paragraph}
              </p>

              {/* <div className="card-grid">
                {siteCopy.section2.bullets.map((item, i) => (
                  <div key={i} className="card">
                    <span>{item}</span>
                  </div>
                ))}
              </div> */}

              <div className="highlight-box">
                <p>
                  {siteCopy.section2.purpose}
                </p>
              </div>
            </motion.div>

            <motion.div {...fadeIn} className="image-col">
              <div className="image-wrapper portrait">
                <img
                  src={assets.relivency}
                  alt="Bridge of Knowledge"
                />
                <div className="image-gradient" />
              </div>
              <div className="caption-box">
                "{siteCopy.section2.refinements.poetic}"
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Section 3: Career Paths */}
      <section id="careers" className="section" ref={opportunityRef}>
        <div className="container">
          <div className="center-header">
            <motion.div {...fadeIn}>
              <div className="section-header centered">
                {/* <Brain className="icon-accent" /> */}
                <span className="overline">Future Pathways</span>
              </div>
              <h2 className="section-title">
                {siteCopy.section3.headline}
              </h2>
              <h3 className="section-subtitle">
                {siteCopy.section3.subheading}
              </h3>
            </motion.div>
          </div>

          <div className="grid-2">
            <motion.div {...fadeIn} className="image-col order-2">
              <div className="image-wrapper square">
                <img
                  src={assets.career}
                  alt="Future Scholar"
                />
              </div>
            </motion.div>

            <motion.div {...fadeIn} className="text-col order-1">
              <p className="section-text">
                {siteCopy.section3.paragraph}
              </p>

              {/* <div className="list-group">
                {siteCopy.section3.bullets.map((item, i) => (
                  <div key={i} className="list-item">
                    <div className="icon-circle">
                    </div>
                    <span>{item}</span>
                  </div>
                ))}
              </div> */}

              <div className="info-card">
                <div className="flex-row">
                  {/* <Lightbulb className="icon-accent" /> */}
                  <div>
                    <p className="info-title">
                      {siteCopy.section3.purpose}
                    </p>
                    <p className="info-subtitle">
                      "{siteCopy.section3.refinements.poetic}"
                    </p>
                  </div>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="footer">
        <div className="container footer-content">
           <span>Hikmah.ai</span>
          <div className="footer-links">
            <a href="https://www.linkedin.com/company/110001682/admin/dashboard/">LinkedIn</a>
            <a href="web.facebook.com/profile.php?id=61583374833125" target="blank">Facebook</a>
          </div>
          <div className="copyright">
            © 2025 Hikmah.ai All rights reserved.
          </div>
        </div>
      </footer>
    </div>
  )
}

export default Home
