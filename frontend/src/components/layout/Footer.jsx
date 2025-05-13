import React from 'react';
import { Link } from 'react-router-dom';
import './Footer.css';

/**
 * Footer component - Main site footer with modern, minimalist design
 */
function Footer() {
  const currentYear = new Date().getFullYear();
  
  return (
    <footer className="footer">
      <div className="container footer__container">
        <div className="footer__content">
          <div className="footer__brand">
            <Link to="/" className="footer__logo">
              TranscriptV2
            </Link>
            <p className="footer__tagline">
              Improve your transcription skills with YouTube videos
            </p>
            <div className="footer__social">
              <a href="https://twitter.com" className="footer__social-link" target="_blank" rel="noopener noreferrer" aria-label="Twitter">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M23 3a10.9 10.9 0 0 1-3.14 1.53 4.48 4.48 0 0 0-7.86 3v1A10.66 10.66 0 0 1 3 4s-4 9 5 13a11.64 11.64 0 0 1-7 2c9 5 20 0 20-11.5a4.5 4.5 0 0 0-.08-.83A7.72 7.72 0 0 0 23 3z"></path></svg>
              </a>
              <a href="https://github.com" className="footer__social-link" target="_blank" rel="noopener noreferrer" aria-label="GitHub">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M9 19c-5 1.5-5-2.5-7-3m14 6v-3.87a3.37 3.37 0 0 0-.94-2.61c3.14-.35 6.44-1.54 6.44-7A5.44 5.44 0 0 0 20 4.77 5.07 5.07 0 0 0 19.91 1S18.73.65 16 2.48a13.38 13.38 0 0 0-7 0C6.27.65 5.09 1 5.09 1A5.07 5.07 0 0 0 5 4.77a5.44 5.44 0 0 0-1.5 3.78c0 5.42 3.3 6.61 6.44 7A3.37 3.37 0 0 0 9 18.13V22"></path></svg>
              </a>
              <a href="https://linkedin.com" className="footer__social-link" target="_blank" rel="noopener noreferrer" aria-label="LinkedIn">
                <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24" height="24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round"><path d="M16 8a6 6 0 0 1 6 6v7h-4v-7a2 2 0 0 0-2-2 2 2 0 0 0-2 2v7h-4v-7a6 6 0 0 1 6-6z"></path><rect x="2" y="9" width="4" height="12"></rect><circle cx="4" cy="4" r="2"></circle></svg>
              </a>
            </div>
          </div>
          
          <div className="footer__links-container">
            <div className="footer__links-column">
              <h3 className="footer__heading">Navigation</h3>
              <ul className="footer__links">
                <li className="footer__link-item">
                  <Link to="/" className="footer__link">Home</Link>
                </li>
                <li className="footer__link-item">
                  <Link to="/dashboard" className="footer__link">Dashboard</Link>
                </li>
                <li className="footer__link-item">
                  <Link to="/search" className="footer__link">Videos</Link>
                </li>
              </ul>
            </div>
            
            <div className="footer__links-column">
              <h3 className="footer__heading">Account</h3>
              <ul className="footer__links">
                <li className="footer__link-item">
                  <Link to="/login" className="footer__link">Login</Link>
                </li>
                <li className="footer__link-item">
                  <Link to="/register" className="footer__link">Register</Link>
                </li>
                <li className="footer__link-item">
                  <Link to="/subscription" className="footer__link">Subscription</Link>
                </li>
              </ul>
            </div>
            
            <div className="footer__links-column">
              <h3 className="footer__heading">Legal</h3>
              <ul className="footer__links">
                <li className="footer__link-item">
                  <Link to="/terms" className="footer__link">Terms of Service</Link>
                </li>
                <li className="footer__link-item">
                  <Link to="/privacy" className="footer__link">Privacy Policy</Link>
                </li>
                <li className="footer__link-item">
                  <Link to="/contact" className="footer__link">Contact Us</Link>
                </li>
              </ul>
            </div>
          </div>
        </div>
        
        <div className="footer__bottom">
          <p className="footer__copyright">
            &copy; {currentYear} TranscriptV2. All rights reserved.
          </p>
          <div className="footer__disclaimer">
            <p className="footer__disclaimer-text">
              Not affiliated with YouTube or Google.
            </p>
          </div>
        </div>
      </div>
    </footer>
  );
}

export default Footer; 