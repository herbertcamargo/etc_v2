import React from 'react';
import { Link } from 'react-router-dom';
import './SubscriptionNotification.css';

/**
 * SubscriptionNotification component - Displays subscription status in header
 * 
 * Shows a badge with subscription status and provides a quick link to subscription page
 */
const SubscriptionNotification = ({ subscription, usage }) => {
  if (!usage) return null;
  
  const { plan_type, is_limited } = usage;
  
  // Determine badge appearance based on subscription status
  const getBadgeClass = () => {
    switch (plan_type) {
      case 'month':
      case 'year':
        return 'subscription-badge--premium';
      case 'free':
      default:
        return 'subscription-badge--free';
    }
  };
  
  // Format plan name for display
  const getPlanName = () => {
    switch (plan_type) {
      case 'month':
        return 'Premium';
      case 'year':
        return 'Premium';
      case 'free':
      default:
        return 'Free Plan';
    }
  };
  
  // Get short text for the badge
  const getBadgeText = () => {
    if (is_limited) {
      return usage.transcriptions_remaining <= 0 
        ? 'Limit Reached' 
        : `${usage.transcriptions_remaining} Left`;
    } else {
      return 'Premium';
    }
  };
  
  return (
    <Link 
      to="/subscription" 
      className={`subscription-badge ${getBadgeClass()}`}
      title={`${getPlanName()} - Click to manage subscription`}
    >
      <span className="subscription-badge__icon">
        {plan_type === 'free' ? '⚡' : '★'}
      </span>
      <span className="subscription-badge__text">
        {getBadgeText()}
      </span>
    </Link>
  );
};

export default SubscriptionNotification; 