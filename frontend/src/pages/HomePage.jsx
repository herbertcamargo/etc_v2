import React from 'react';
import { Link } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import './HomePage.css';

function HomePage() {
  return (
    <Layout>
      <section className="hero">
        <div className="container">
          <div className="hero__content">
            <h1 className="hero__title">
              Improve Your <span className="hero__title-highlight">Transcription</span> Skills
            </h1>
            <p className="hero__subtitle">
              Practice transcribing YouTube videos with real-time feedback and accuracy tracking.
              Perfect for students, professionals, and language learners.
            </p>
            <div className="hero__actions">
              <Link to="/register" className="button button--primary hero__button">
                Get Started
              </Link>
              <Link to="/search" className="button button--secondary hero__button">
                Browse Videos
              </Link>
            </div>
          </div>
          <div className="hero__image-container">
            <img 
              src="/assets/hero-image.svg" 
              alt="Transcription illustration" 
              className="hero__image fade-in" 
            />
            <div className="hero__decoration hero__decoration--1"></div>
            <div className="hero__decoration hero__decoration--2"></div>
          </div>
        </div>
      </section>

      <section className="features section">
        <div className="container">
          <h2 className="section-title">How It Works</h2>
          <div className="features__grid">
            <div className="feature-card fade-in">
              <div className="feature-card__icon-container">
                <svg className="feature-card__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <circle cx="11" cy="11" r="8"></circle>
                  <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
              </div>
              <h3 className="feature-card__title">Search Videos</h3>
              <p className="feature-card__description">
                Browse our curated collection of YouTube videos or search for specific content that matches your interests.
              </p>
            </div>
            <div className="feature-card fade-in" style={{ animationDelay: '0.1s' }}>
              <div className="feature-card__icon-container">
                <svg className="feature-card__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <path d="M12 20h9"></path>
                  <path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"></path>
                </svg>
              </div>
              <h3 className="feature-card__title">Transcribe Content</h3>
              <p className="feature-card__description">
                Listen carefully and type what you hear as the video plays, developing your ear and typing skills.
              </p>
            </div>
            <div className="feature-card fade-in" style={{ animationDelay: '0.2s' }}>
              <div className="feature-card__icon-container">
                <svg className="feature-card__icon" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                  <polyline points="22 12 18 12 15 21 9 3 6 12 2 12"></polyline>
                </svg>
              </div>
              <h3 className="feature-card__title">Track Progress</h3>
              <p className="feature-card__description">
                Receive word-by-word accuracy feedback and detailed statistics to monitor your improvement over time.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="testimonials section">
        <div className="container">
          <h2 className="section-title">What Users Say</h2>
          <div className="testimonials__grid">
            <div className="testimonial-card fade-in">
              <div className="testimonial-card__content">
                <p className="testimonial-card__quote">
                  "This platform has significantly improved my listening comprehension. The real-time feedback is incredibly helpful."
                </p>
                <div className="testimonial-card__author">
                  <div className="testimonial-card__avatar">JD</div>
                  <div className="testimonial-card__info">
                    <span className="testimonial-card__name">Jane Doe</span>
                    <span className="testimonial-card__title">Language Student</span>
                  </div>
                </div>
              </div>
            </div>
            <div className="testimonial-card fade-in" style={{ animationDelay: '0.1s' }}>
              <div className="testimonial-card__content">
                <p className="testimonial-card__quote">
                  "As a journalist, accurate transcription is essential. This tool has helped me improve my speed and precision."
                </p>
                <div className="testimonial-card__author">
                  <div className="testimonial-card__avatar">MS</div>
                  <div className="testimonial-card__info">
                    <span className="testimonial-card__name">Michael Smith</span>
                    <span className="testimonial-card__title">Journalist</span>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <section className="cta section">
        <div className="container">
          <div className="cta__content">
            <h2 className="cta__title">Ready to Improve Your Skills?</h2>
            <p className="cta__description">
              Join thousands of users who are enhancing their transcription abilities with our platform.
            </p>
            <Link to="/register" className="button button--primary cta__button">
              Start Free Today
            </Link>
          </div>
        </div>
      </section>
    </Layout>
  );
}

export default HomePage; 