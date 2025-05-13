import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Layout from '../components/layout/Layout';
import PlanCard from '../components/subscription/PlanCard';
import SubscriptionUsage from '../components/subscription/SubscriptionUsage';
import PaymentForm from '../components/subscription/PaymentForm';
import { 
  getSubscriptionPlans, 
  getCurrentSubscription, 
  cancelSubscription,
  getSubscriptionUsage
} from '../services/subscriptionService';
import { useAuth } from '../contexts/AuthContext';
import './SubscriptionPage.css';

/**
 * SubscriptionPage component - Manages user subscription plans and checkout
 */
function SubscriptionPage() {
  const { user } = useAuth();
  const navigate = useNavigate();
  
  const [plans, setPlans] = useState([]);
  const [selectedPlanId, setSelectedPlanId] = useState(null);
  const [currentSubscription, setCurrentSubscription] = useState(null);
  const [usageStats, setUsageStats] = useState(null);
  const [showPaymentForm, setShowPaymentForm] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [isCancelling, setIsCancelling] = useState(false);
  const [error, setError] = useState(null);
  
  // Load plans and subscription data
  useEffect(() => {
    loadData();
  }, []);
  
  const loadData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Load subscription plans
      const plansResponse = await getSubscriptionPlans();
      setPlans(plansResponse.data);
      
      // Load current subscription if any
      const subscriptionResponse = await getCurrentSubscription();
      setCurrentSubscription(subscriptionResponse.data);
      
      // Load usage statistics
      const usageResponse = await getSubscriptionUsage();
      setUsageStats(usageResponse.data);
    } catch (err) {
      console.error('Subscription data loading error:', err);
      setError('Failed to load subscription data. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };
  
  const handlePlanSelect = (planId) => {
    setSelectedPlanId(planId);
    setShowPaymentForm(true);
  };
  
  const handlePaymentStart = () => {
    // Nothing to do here, we'll redirect to Stripe
  };
  
  const handlePaymentCancel = () => {
    setShowPaymentForm(false);
    setSelectedPlanId(null);
  };
  
  const handleSubscriptionCancel = async () => {
    if (!window.confirm('Are you sure you want to cancel your subscription? Your premium access will end at the end of your current billing period.')) {
      return;
    }
    
    setIsCancelling(true);
    
    try {
      await cancelSubscription();
      await loadData(); // Reload data to show updated subscription status
    } catch (err) {
      console.error('Subscription cancellation error:', err);
      setError('Failed to cancel subscription. Please try again.');
    } finally {
      setIsCancelling(false);
    }
  };
  
  // Determine if the user has an active subscription
  const hasActiveSubscription = currentSubscription && currentSubscription.status === 'active';
  
  return (
    <Layout>
      <div className="subscription-page">
        <div className="subscription-page__header">
          <h1 className="subscription-page__title">Subscription</h1>
          <p className="subscription-page__subtitle">
            {hasActiveSubscription 
              ? 'Manage your subscription and usage'
              : 'Choose a subscription plan to unlock unlimited transcriptions'}
          </p>
        </div>
        
        {error && (
          <div className="subscription-page__error">
            {error}
            <button 
              className="button button--text subscription-page__error-dismiss" 
              onClick={() => setError(null)}
            >
              Dismiss
            </button>
          </div>
        )}
        
        {isLoading ? (
          <div className="subscription-page__loading">
            <div className="loader"></div>
            <p>Loading subscription data...</p>
          </div>
        ) : (
          <>
            {/* Current subscription and usage info */}
            {usageStats && (
              <div className="subscription-page__usage-section">
                <SubscriptionUsage usage={usageStats} />
                
                {hasActiveSubscription && (
                  <div className="subscription-page__current-subscription">
                    <h3 className="subscription-page__section-title">Current Subscription</h3>
                    <div className="subscription-page__subscription-details">
                      <div className="subscription-page__detail">
                        <span className="subscription-page__detail-label">Plan</span>
                        <span className="subscription-page__detail-value">
                          {currentSubscription.plan_type === 'month' ? 'Monthly' : 'Yearly'} Premium
                        </span>
                      </div>
                      <div className="subscription-page__detail">
                        <span className="subscription-page__detail-label">Status</span>
                        <span className="subscription-page__detail-value subscription-page__status">
                          <span className="subscription-page__status-dot"></span>
                          {currentSubscription.status === 'active' ? 'Active' : 'Inactive'}
                        </span>
                      </div>
                      <div className="subscription-page__detail">
                        <span className="subscription-page__detail-label">Renews</span>
                        <span className="subscription-page__detail-value">
                          {new Date(currentSubscription.end_date).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                    
                    <button 
                      className="button button--danger subscription-page__cancel-button"
                      onClick={handleSubscriptionCancel}
                      disabled={isCancelling}
                    >
                      {isCancelling ? 'Cancelling...' : 'Cancel Subscription'}
                    </button>
                  </div>
                )}
              </div>
            )}
            
            {/* Plan selection */}
            {!hasActiveSubscription && !showPaymentForm && (
              <div className="subscription-page__plans-section">
                <h2 className="subscription-page__section-title">Available Plans</h2>
                <div className="subscription-page__plans-grid">
                  {plans.map(plan => (
                    <PlanCard
                      key={plan.id}
                      plan={plan}
                      isSelected={selectedPlanId === plan.id}
                      onSelect={handlePlanSelect}
                    />
                  ))}
                </div>
              </div>
            )}
            
            {/* Payment form */}
            {showPaymentForm && (
              <div className="subscription-page__payment-section">
                <PaymentForm
                  selectedPlanId={selectedPlanId}
                  onPaymentStart={handlePaymentStart}
                  onPaymentCancel={handlePaymentCancel}
                  onError={setError}
                />
              </div>
            )}
            
            {/* Free tier info */}
            {!hasActiveSubscription && (
              <div className="subscription-page__free-info">
                <h3 className="subscription-page__free-title">Free Tier</h3>
                <p className="subscription-page__free-description">
                  You can use our service for free with a limit of 3 transcriptions.
                  Upgrade to a premium plan for unlimited transcriptions and more features.
                </p>
              </div>
            )}
          </>
        )}
      </div>
    </Layout>
  );
}

export default SubscriptionPage; 