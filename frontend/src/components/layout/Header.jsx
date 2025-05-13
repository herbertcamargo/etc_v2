import React, { useState, useEffect } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../../contexts/AuthContext';
import { useTheme } from '../../contexts/ThemeContext';
import SubscriptionNotification from '../subscription/SubscriptionNotification';
import { getCurrentSubscription, getSubscriptionUsage } from '../../services/subscriptionService';
import './Header.css';

/**
 * Header component - Main navigation and app header
 * Modern, minimalist design with streamlined navigation
 */
function Header() {
  const { user, isAuthenticated, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();
  const location = useLocation();
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [userMenuOpen, setUserMenuOpen] = useState(false);
  const [subscription, setSubscription] = useState(null);
  const [usageStats, setUsageStats] = useState(null);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    // Fetch subscription data when user is authenticated
    if (isAuthenticated) {
      fetchSubscriptionData();
    }
  }, [isAuthenticated]);

  useEffect(() => {
    // Add scroll event listener to apply shadow on scroll
    const handleScroll = () => {
      setScrolled(window.scrollY > 10);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  useEffect(() => {
    // Close mobile menu on route change
    setMobileMenuOpen(false);
    setUserMenuOpen(false);
  }, [location.pathname]);

  const fetchSubscriptionData = async () => {
    try {
      // Get current subscription (if any)
      const subscriptionResponse = await getCurrentSubscription();
      setSubscription(subscriptionResponse.data);
      
      // Get subscription usage statistics
      const usageResponse = await getSubscriptionUsage();
      setUsageStats(usageResponse.data);
    } catch (error) {
      console.error('Error fetching subscription data:', error);
    }
  };

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const toggleMobileMenu = () => {
    setMobileMenuOpen(!mobileMenuOpen);
    if (userMenuOpen) setUserMenuOpen(false);
  };

  const toggleUserMenu = () => {
    setUserMenuOpen(!userMenuOpen);
  };

  return (
    <header className={`header ${scrolled ? 'header--scrolled' : ''}`}>
      <div className="container header__container">
        <div className="header__logo">
          <Link to="/" className="header__logo-link">
            TranscriptV2
          </Link>
        </div>

        {/* Mobile menu toggle button */}
        <button 
          className="header__mobile-toggle hide-desktop" 
          onClick={toggleMobileMenu}
          aria-label={mobileMenuOpen ? 'Close menu' : 'Open menu'}
        >
          <span className={`hamburger ${mobileMenuOpen ? 'hamburger--active' : ''}`}></span>
        </button>

        {/* Navigation */}
        <nav className={`header__nav ${mobileMenuOpen ? 'header__nav--active' : ''}`}>
          <ul className="header__nav-list">
            <li className="header__nav-item">
              <Link to="/" className={`header__nav-link ${location.pathname === '/' ? 'header__nav-link--active' : ''}`}>
                Home
              </Link>
            </li>
            
            {isAuthenticated ? (
              <>
                <li className="header__nav-item">
                  <Link to="/dashboard" className={`header__nav-link ${location.pathname === '/dashboard' ? 'header__nav-link--active' : ''}`}>
                    Dashboard
                  </Link>
                </li>
                <li className="header__nav-item">
                  <Link to="/search" className={`header__nav-link ${location.pathname === '/search' ? 'header__nav-link--active' : ''}`}>
                    Videos
                  </Link>
                </li>
              </>
            ) : (
              <li className="header__nav-item">
                <Link to="/register" className="header__nav-link">
                  Get Started
                </Link>
              </li>
            )}
          </ul>

          {/* User menu or auth links */}
          <div className="header__actions">
            {/* Theme toggle button */}
            <button 
              className="header__theme-toggle" 
              onClick={toggleTheme} 
              aria-label={`Switch to ${theme === 'light' ? 'dark' : 'light'} theme`}
            >
              {theme === 'light' ? '🌙' : '☀️'}
            </button>

            {isAuthenticated ? (
              <>
                {/* Subscription notification for authenticated users */}
                {usageStats && (
                  <SubscriptionNotification 
                    subscription={subscription} 
                    usage={usageStats} 
                  />
                )}
                
                {/* User menu */}
                <div className="header__user-menu">
                  <button 
                    className="header__user-button" 
                    onClick={toggleUserMenu}
                    aria-label="Open user menu"
                  >
                    <div className="header__user-avatar">
                      {user?.username.charAt(0).toUpperCase()}
                    </div>
                    <span className="header__username hide-mobile">{user?.username}</span>
                  </button>
                  {userMenuOpen && (
                    <div className="header__dropdown fade-in">
                      <div className="header__dropdown-header">
                        <span className="header__dropdown-name">{user?.username}</span>
                        <span className="header__dropdown-email">{user?.email}</span>
                      </div>
                      <div className="header__dropdown-divider"></div>
                      <Link to="/dashboard" className="header__dropdown-item">
                        Dashboard
                      </Link>
                      <Link to="/settings" className="header__dropdown-item">
                        Settings
                      </Link>
                      <Link to="/subscription" className="header__dropdown-item">
                        Subscription
                      </Link>
                      <div className="header__dropdown-divider"></div>
                      <button className="header__dropdown-item header__logout" onClick={handleLogout}>
                        Logout
                      </button>
                    </div>
                  )}
                </div>
              </>
            ) : (
              <div className="header__auth-links">
                <Link to="/login" className="header__login-link">
                  Login
                </Link>
                <Link to="/register" className="button button--primary header__register-button">
                  Register
                </Link>
              </div>
            )}
          </div>
        </nav>
      </div>
    </header>
  );
}

export default Header; 