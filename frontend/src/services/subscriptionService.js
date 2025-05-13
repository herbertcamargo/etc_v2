/**
 * Subscription Service
 * 
 * This module provides functions for interacting with the subscription API endpoints.
 * It handles retrieving subscription plans, managing user subscriptions, and checkout processes.
 */
import api from './api';

/**
 * Get available subscription plans
 * 
 * @returns {Promise} Promise resolving to available subscription plans
 */
export const getSubscriptionPlans = async () => {
  return api.get('/subscriptions/plans');
};

/**
 * Get the current user's subscription
 * 
 * @returns {Promise} Promise resolving to the current user's subscription
 */
export const getCurrentSubscription = async () => {
  try {
    return await api.get('/subscriptions/me');
  } catch (error) {
    if (error.response && error.response.status === 404) {
      // No active subscription found, return null
      return { data: null };
    }
    throw error;
  }
};

/**
 * Cancel the current user's subscription
 * 
 * @returns {Promise} Promise resolving when subscription is canceled
 */
export const cancelSubscription = async () => {
  return api.delete('/subscriptions/me');
};

/**
 * Create a checkout session for subscription payment
 * 
 * @param {Object} checkoutData - Data for creating the checkout session
 * @param {string} checkoutData.price_id - ID of the selected plan
 * @param {string} checkoutData.success_url - URL to redirect after successful payment
 * @param {string} checkoutData.cancel_url - URL to redirect after canceled payment
 * @returns {Promise} Promise resolving to checkout session data
 */
export const createCheckoutSession = async (checkoutData) => {
  return api.post('/subscriptions/checkout', checkoutData);
};

/**
 * Get subscription usage statistics
 * 
 * @returns {Promise} Promise resolving to usage statistics
 */
export const getSubscriptionUsage = async () => {
  return api.get('/subscriptions/usage');
}; 