import React from 'react';
import './SubscriptionUsage.css';

/**
 * SubscriptionUsage component - Displays subscription usage statistics
 * 
 * Shows information about the user's subscription plan, usage limits, and renewal date
 */
const SubscriptionUsage = ({ usage }) => {
  if (!usage) return null;
  
  const { 
    plan_type, 
    transcriptions_used, 
    transcriptions_limit, 
    transcriptions_remaining,
    is_limited, 
    renewal_date 
  } = usage;
  
  // Format the renewal date
  const formatRenewalDate = (dateString) => {
    if (!dateString) return 'N/A';
    
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('en-US', {
      year: 'numeric',
      month: 'long',
      day: 'numeric'
    }).format(date);
  };
  
  // Calculate usage percentage for the progress bar
  const calculateUsagePercentage = () => {
    if (!is_limited || transcriptions_limit === 0) return 0;
    
    const percentage = (transcriptions_used / transcriptions_limit) * 100;
    return Math.min(percentage, 100); // Cap at 100%
  };
  
  // Format the plan type for display
  const formatPlanType = (planType) => {
    switch (planType) {
      case 'free':
        return 'Free Plan';
      case 'month':
        return 'Monthly Premium';
      case 'year':
        return 'Yearly Premium';
      default:
        return 'Unknown Plan';
    }
  };
  
  // Format the limit for display
  const formatLimit = (limit) => {
    return Number.isFinite(limit) ? limit.toString() : 'Unlimited';
  };
  
  return (
    <div className="subscription-usage">
      <div className="subscription-usage__header">
        <h3 className="subscription-usage__title">Subscription Usage</h3>
        <div className={`subscription-usage__plan-badge subscription-usage__plan-badge--${plan_type}`}>
          {formatPlanType(plan_type)}
        </div>
      </div>
      
      <div className="subscription-usage__stats">
        <div className="subscription-usage__stat">
          <span className="subscription-usage__stat-label">Transcriptions Used</span>
          <span className="subscription-usage__stat-value">{transcriptions_used}</span>
        </div>
        
        <div className="subscription-usage__stat">
          <span className="subscription-usage__stat-label">Limit</span>
          <span className="subscription-usage__stat-value">{formatLimit(transcriptions_limit)}</span>
        </div>
        
        <div className="subscription-usage__stat">
          <span className="subscription-usage__stat-label">Remaining</span>
          <span className="subscription-usage__stat-value">
            {is_limited ? transcriptions_remaining : '∞'}
          </span>
        </div>
        
        {renewal_date && (
          <div className="subscription-usage__stat">
            <span className="subscription-usage__stat-label">Renewal Date</span>
            <span className="subscription-usage__stat-value">{formatRenewalDate(renewal_date)}</span>
          </div>
        )}
      </div>
      
      {is_limited && (
        <div className="subscription-usage__progress-container">
          <div className="subscription-usage__progress-bar">
            <div 
              className="subscription-usage__progress-fill"
              style={{ width: `${calculateUsagePercentage()}%` }}
            />
          </div>
          <div className="subscription-usage__progress-text">
            {transcriptions_used} of {transcriptions_limit} transcriptions used
          </div>
        </div>
      )}
    </div>
  );
};

export default SubscriptionUsage;