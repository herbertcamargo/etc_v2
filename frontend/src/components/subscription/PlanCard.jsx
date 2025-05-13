import React from 'react';
import './PlanCard.css';

/**
 * PlanCard component - Displays a subscription plan's details
 * 
 * Shows plan information, pricing, and features with a select button
 */
const PlanCard = ({ 
  plan, 
  isSelected = false, 
  onSelect, 
  isLoading = false 
}) => {
  if (!plan) return null;
  
  const { 
    id, 
    name, 
    description, 
    price, 
    currency = 'USD', 
    interval, 
    features = [] 
  } = plan;
  
  // Format currency display
  const formatCurrency = (amount) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency,
      minimumFractionDigits: 2
    }).format(amount);
  };
  
  // Format interval display
  const formatInterval = (interval) => {
    return interval === 'month' ? 'monthly' : 'yearly';
  };
  
  return (
    <div className={`plan-card ${isSelected ? 'plan-card--selected' : ''}`}>
      <div className="plan-card__header">
        <h3 className="plan-card__name">{name}</h3>
        <p className="plan-card__description">{description}</p>
      </div>
      
      <div className="plan-card__pricing">
        <span className="plan-card__price">{formatCurrency(price)}</span>
        <span className="plan-card__interval">/{formatInterval(interval)}</span>
      </div>
      
      <ul className="plan-card__features">
        {features.map((feature, index) => (
          <li key={index} className="plan-card__feature">
            <span className="plan-card__feature-icon">✓</span>
            <span className="plan-card__feature-text">{feature}</span>
          </li>
        ))}
      </ul>
      
      <div className="plan-card__actions">
        <button 
          className={`button ${isSelected ? 'button--secondary' : 'button--primary'}`}
          onClick={() => onSelect && onSelect(id)}
          disabled={isLoading}
        >
          {isLoading ? 'Processing...' : (isSelected ? 'Selected' : 'Select Plan')}
        </button>
      </div>
    </div>
  );
};

export default PlanCard; 