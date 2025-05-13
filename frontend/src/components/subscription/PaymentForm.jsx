import React, { useState } from 'react';
import { createCheckoutSession } from '../../services/subscriptionService';
import './PaymentForm.css';

/**
 * PaymentForm component - Handles redirection to Stripe checkout
 * 
 * This component initiates a Stripe checkout session for subscription payment
 */
const PaymentForm = ({ 
  selectedPlanId, 
  onPaymentStart, 
  onPaymentCancel, 
  onError 
}) => {
  const [isProcessing, setIsProcessing] = useState(false);
  
  // Handle checkout button click
  const handleCheckout = async () => {
    if (!selectedPlanId) {
      onError && onError('Please select a subscription plan');
      return;
    }
    
    setIsProcessing(true);
    
    try {
      // Notify parent component that payment is starting
      onPaymentStart && onPaymentStart();
      
      // Create the checkout data with success and cancel URLs
      const checkoutData = {
        price_id: selectedPlanId,
        success_url: `${window.location.origin}/subscription/success`,
        cancel_url: `${window.location.origin}/subscription`
      };
      
      // Create the checkout session
      const response = await createCheckoutSession(checkoutData);
      
      // Redirect to Stripe checkout page
      window.location.href = response.data.checkout_url;
    } catch (error) {
      console.error('Checkout error:', error);
      setIsProcessing(false);
      
      // Handle error
      const errorMessage = 
        error.response?.data?.detail || 
        'An error occurred during checkout. Please try again.';
      
      onError && onError(errorMessage);
    }
  };
  
  const handleCancel = () => {
    onPaymentCancel && onPaymentCancel();
  };
  
  return (
    <div className="payment-form">
      <div className="payment-form__content">
        <h3 className="payment-form__title">Complete Your Subscription</h3>
        
        <p className="payment-form__description">
          You'll be redirected to Stripe, our secure payment processor, to complete your subscription.
        </p>
        
        <div className="payment-form__secure-badge">
          <span className="payment-form__secure-icon">🔒</span>
          <span className="payment-form__secure-text">Secure Checkout with Stripe</span>
        </div>
        
        <div className="payment-form__actions">
          <button 
            className="button button--primary payment-form__checkout-btn"
            onClick={handleCheckout}
            disabled={isProcessing || !selectedPlanId}
          >
            {isProcessing ? 'Processing...' : 'Proceed to Checkout'}
          </button>
          
          <button 
            className="button button--text payment-form__cancel-btn"
            onClick={handleCancel}
            disabled={isProcessing}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
};

export default PaymentForm; 