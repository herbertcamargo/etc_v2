import React, { useEffect, useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import './SubscriptionSuccessPage.css';

/**
 * SubscriptionSuccessPage component - Displayed after successful Stripe payment
 * 
 * This component is shown when the user is redirected back from a successful
 * Stripe checkout session. It displays a success message and provides navigation options.
 */
function SubscriptionSuccessPage() {
  const navigate = useNavigate();
  const location = useLocation();
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Check if the URL has a session_id parameter from Stripe
    const queryParams = new URLSearchParams(location.search);
    const sessionId = queryParams.get('session_id');
    
    if (!sessionId) {
      setError('No session information found. Please check your subscription status in your account.');
      setIsLoading(false);
      return;
    }
    
    // We don't need to verify with the backend as the webhook will handle
    // updating the subscription status in the database
    setIsLoading(false);
    
    // Automatically redirect to dashboard after 5 seconds
    const redirectTimer = setTimeout(() => {
      navigate('/dashboard');
    }, 5000);
    
    return () => clearTimeout(redirectTimer);
  }, [location, navigate]);
  
  return (
    <Layout>
      <div className="subscription-success">
        {isLoading ? (
          <div className="subscription-success__loading">
            <div className="loader"></div>
            <p>Processing your subscription...</p>
          </div>
        ) : error ? (
          <div className="subscription-success__error">
            <h2>Something went wrong</h2>
            <p>{error}</p>
            <Link to="/subscription" className="button button--primary">
              Return to Subscription Page
            </Link>
          </div>
        ) : (
          <div className="subscription-success__content">
            <div className="subscription-success__icon">✓</div>
            <h1 className="subscription-success__title">Subscription Activated!</h1>
            <p className="subscription-success__message">
              Thank you for subscribing! Your premium features are now available.
            </p>
            <p className="subscription-success__submessage">
              You will be redirected to the dashboard in a few seconds.
            </p>
            <div className="subscription-success__actions">
              <Link to="/dashboard" className="button button--primary">
                Go to Dashboard
              </Link>
              <Link to="/subscription" className="button button--secondary">
                View Subscription Details
              </Link>
            </div>
          </div>
        )}
      </div>
    </Layout>
  );
}

export default SubscriptionSuccessPage; 